"""Flask web application for reference-free k-mer counting and SIG-mer candidate discovery."""
from flask import Flask, render_template_string, request

from kmer_logic import K, clean_sequence, count_kmers, load_sample_reads, validate_sequence

app = Flask(__name__)

HTML_TEMPLATE = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>SIG-mer Explorer | Reference-Free k-mer Counter</title>
    <meta name="description" content="Lightweight bioinformatics web tool for reference-free DNA k-mer extraction, frequency counting, and SIG-mer candidate identification.">
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=IBM+Plex+Mono:wght@400;600&family=Inter:wght@400;500;600;700&display=swap" rel="stylesheet">
    <style>
        :root {
            --bg-page: hsl(210, 25%, 97%);
            --bg-surface: hsl(0, 0%, 100%);
            --bg-subtle: hsl(210, 22%, 94%);
            --text-primary: hsl(215, 28%, 14%);
            --text-secondary: hsl(215, 16%, 42%);
            --accent: hsl(174, 72%, 28%);
            --accent-hover: hsl(174, 76%, 22%);
            --accent-soft: hsl(174, 45%, 92%);
            --border-color: hsl(214, 20%, 86%);
            --error-bg: hsl(0, 75%, 96%);
            --error-text: hsl(0, 68%, 34%);
            --radius: 8px;
        }

        * {
            box-sizing: border-box;
            margin: 0;
            padding: 0;
        }

        body {
            font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
            background-color: var(--bg-page);
            color: var(--text-primary);
            line-height: 1.6;
            padding: 2.5rem 1.25rem;
        }

        .container {
            max-width: 860px;
            margin: 0 auto;
        }

        header {
            margin-bottom: 2rem;
            border-bottom: 1px solid var(--border-color);
            padding-bottom: 1.25rem;
        }

        h1 {
            font-size: 1.75rem;
            font-weight: 700;
            letter-spacing: -0.02em;
            color: var(--text-primary);
            margin-bottom: 0.35rem;
        }

        .subtitle {
            color: var(--text-secondary);
            font-size: 0.95rem;
        }

        .panel {
            background: var(--bg-surface);
            border: 1px solid var(--border-color);
            border-radius: var(--radius);
            padding: 1.5rem;
            margin-bottom: 1.5rem;
            box-shadow: 0 2px 6px rgba(15, 23, 42, 0.04);
        }

        .form-grid {
            display: grid;
            grid-template-columns: 1fr 160px;
            gap: 1rem;
            margin-bottom: 1rem;
        }

        @media (max-width: 640px) {
            .form-grid {
                grid-template-columns: 1fr;
            }
        }

        label {
            display: block;
            font-size: 0.875rem;
            font-weight: 600;
            margin-bottom: 0.4rem;
            color: var(--text-primary);
        }

        select, input[type="number"], textarea {
            width: 100%;
            font-family: inherit;
            font-size: 0.95rem;
            padding: 0.625rem 0.75rem;
            border: 1px solid var(--border-color);
            border-radius: 6px;
            background: var(--bg-surface);
            color: var(--text-primary);
            transition: border-color 0.15s ease, box-shadow 0.15s ease;
        }

        textarea {
            font-family: 'IBM Plex Mono', monospace;
            font-size: 0.9rem;
            letter-spacing: 0.04em;
            resize: vertical;
            min-height: 92px;
        }

        select:focus, input[type="number"]:focus, textarea:focus {
            outline: none;
            border-color: var(--accent);
            box-shadow: 0 0 0 3px var(--accent-soft);
        }

        .actions {
            display: flex;
            align-items: center;
            justify-content: space-between;
            flex-wrap: wrap;
            gap: 0.75rem;
            margin-top: 1rem;
        }

        .btn-primary {
            background-color: var(--accent);
            color: #ffffff;
            font-weight: 600;
            font-size: 0.95rem;
            padding: 0.65rem 1.35rem;
            border: none;
            border-radius: 6px;
            cursor: pointer;
            transition: background-color 0.15s ease, transform 0.1s ease;
        }

        .btn-primary:hover {
            background-color: var(--accent-hover);
        }

        .btn-primary:active {
            transform: translateY(1px);
        }

        .hint {
            font-size: 0.82rem;
            color: var(--text-secondary);
        }

        .alert-error {
            background: var(--error-bg);
            color: var(--error-text);
            padding: 0.875rem 1rem;
            border-radius: var(--radius);
            font-size: 0.9rem;
            font-weight: 500;
            margin-bottom: 1.5rem;
        }

        .summary-bar {
            display: flex;
            flex-wrap: wrap;
            gap: 1.5rem;
            padding-bottom: 1.25rem;
            margin-bottom: 1.25rem;
            border-bottom: 1px solid var(--border-color);
        }

        .metric {
            flex: 1;
            min-width: 140px;
        }

        .metric-label {
            font-size: 0.78rem;
            text-transform: uppercase;
            letter-spacing: 0.05em;
            color: var(--text-secondary);
            font-weight: 600;
        }

        .metric-value {
            font-size: 1.35rem;
            font-weight: 700;
            color: var(--text-primary);
            margin-top: 0.15rem;
        }

        .mono {
            font-family: 'IBM Plex Mono', monospace;
            font-weight: 600;
        }

        .top-badge {
            display: inline-block;
            background: var(--accent-soft);
            color: var(--accent-hover);
            padding: 0.1rem 0.5rem;
            border-radius: 4px;
            font-family: 'IBM Plex Mono', monospace;
            font-size: 0.95rem;
            font-weight: 600;
        }

        h2 {
            font-size: 1.15rem;
            font-weight: 600;
            margin-bottom: 0.85rem;
        }

        table {
            width: 100%;
            border-collapse: collapse;
            font-size: 0.92rem;
        }

        th, td {
            text-align: left;
            padding: 0.65rem 0.75rem;
            border-bottom: 1px solid var(--border-color);
        }

        th {
            font-size: 0.8rem;
            text-transform: uppercase;
            letter-spacing: 0.04em;
            color: var(--text-secondary);
            background: var(--bg-subtle);
        }

        tbody tr:hover {
            background-color: hsl(210, 25%, 98%);
        }

        .freq-bar-track {
            width: 100%;
            max-width: 180px;
            height: 8px;
            background: var(--bg-subtle);
            border-radius: 4px;
            overflow: hidden;
        }

        .freq-bar-fill {
            height: 100%;
            background: var(--accent);
            border-radius: 4px;
        }
    </style>
</head>
<body>
    <main class="container">
        <header>
            <h1>Reference-Free k-mer &amp; SIG-mer Counter</h1>
            <p class="subtitle">Extract overlapping k-mers from raw DNA sequencing reads and rank top SIG-mer candidates without reference alignment.</p>
        </header>

        <section class="panel" aria-labelledby="form-heading">
            <form id="kmer-form" method="POST" action="/">
                <div class="form-grid">
                    <div>
                        <label for="sample-select">Load Sample Read (from reads.csv)</label>
                        <select id="sample-select" name="sample_id" onchange="applySampleRead(this)">
                            <option value="">-- Custom DNA Sequence --</option>
                            {% for read_id, seq in sample_reads.items() %}
                            <option value="{{ read_id }}" data-seq="{{ seq }}" {% if selected_sample == read_id %}selected{% endif %}>
                                {{ read_id }} ({{ seq[:18] }}... | {{ seq|length }} bp)
                            </option>
                            {% endfor %}
                        </select>
                    </div>
                    <div>
                        <label for="k-input">k-mer Length (k)</label>
                        <input id="k-input" type="number" name="k" min="1" max="32" value="{{ k }}" required>
                    </div>
                </div>

                <div>
                    <label for="sequence-input">DNA Sequence (5' &rarr; 3')</label>
                    <textarea id="sequence-input" name="sequence" placeholder="Enter DNA sequence (A, C, G, T)..." required>{{ sequence }}</textarea>
                </div>

                <div class="actions">
                    <span class="hint">Whitespace is ignored; sequences are automatically normalized to uppercase.</span>
                    <button id="submit-btn" type="submit" class="btn-primary">Count k-mers</button>
                </div>
            </form>
        </section>

        {% if error %}
        <div id="error-message" class="alert-error" role="alert">
            {{ error }}
        </div>
        {% endif %}

        {% if results %}
        <section id="results-panel" class="panel" aria-labelledby="results-heading">
            <div class="summary-bar">
                <div class="metric">
                    <div class="metric-label">Sequence Length</div>
                    <div class="metric-value">{{ sequence|length }} bp</div>
                </div>
                <div class="metric">
                    <div class="metric-label">Total {{ k }}-mers</div>
                    <div class="metric-value">{{ total_kmers }}</div>
                </div>
                <div class="metric">
                    <div class="metric-label">Unique {{ k }}-mers</div>
                    <div class="metric-value">{{ unique_kmers }}</div>
                </div>
                <div class="metric">
                    <div class="metric-label">Top SIG-mer Candidate</div>
                    <div class="metric-value">
                        <span class="top-badge">{{ top_kmer }}</span> ({{ top_count }}&times;)
                    </div>
                </div>
            </div>

            <h2 id="results-heading">Ranked {{ k }}-mer Frequencies</h2>
            <table id="kmer-results-table">
                <thead>
                    <tr>
                        <th>Rank</th>
                        <th>{{ k }}-mer</th>
                        <th>Count</th>
                        <th>Relative Share</th>
                        <th>Distribution</th>
                    </tr>
                </thead>
                <tbody>
                    {% for item in results %}
                    <tr>
                        <td>#{{ item.rank }}</td>
                        <td class="mono">{{ item.kmer }}</td>
                        <td>{{ item.count }}</td>
                        <td>{{ item.percentage }}%</td>
                        <td>
                            <div class="freq-bar-track">
                                <div class="freq-bar-fill" style="width: {{ item.bar_width }}%;"></div>
                            </div>
                        </td>
                    </tr>
                    {% endfor %}
                </tbody>
            </table>
        </section>
        {% endif %}
    </main>

    <script>
        function applySampleRead(selectElem) {
            const selectedOption = selectElem.options[selectElem.selectedIndex];
            const seq = selectedOption.getAttribute('data-seq');
            if (seq) {
                document.getElementById('sequence-input').value = seq;
            }
        }
    </script>
</body>
</html>
"""


@app.route("/", methods=["GET", "POST"])
def index():
    sample_reads = load_sample_reads()
    default_read_id = "read_1" if "read_1" in sample_reads else next(iter(sample_reads), "")
    default_seq = sample_reads.get(default_read_id, "ATGCGATACGCTTGATCGATCGGATCGATACG")

    selected_sample = request.values.get("sample_id", default_read_id if request.method == "GET" else "")
    raw_sequence = request.values.get("sequence", "")

    if not raw_sequence and selected_sample in sample_reads:
        raw_sequence = sample_reads[selected_sample]
    elif request.method == "GET" and not raw_sequence:
        raw_sequence = default_seq

    raw_k = request.values.get("k", str(K))
    try:
        k = int(raw_k)
    except ValueError:
        k = K

    sequence = clean_sequence(raw_sequence)
    if selected_sample and sample_reads.get(selected_sample) != sequence:
        selected_sample = ""

    error = ""
    results = []
    total_kmers = 0
    unique_kmers = 0
    top_kmer = "-"
    top_count = 0

    is_valid, error_msg = validate_sequence(sequence, k)
    if not is_valid:
        error = error_msg
    else:
        counts = count_kmers(sequence, k)
        total_kmers = sum(counts.values())
        unique_kmers = len(counts)
        most_common = counts.most_common()
        if most_common:
            top_kmer, top_count = most_common[0]
            for rank, (kmer_str, count) in enumerate(most_common, start=1):
                pct = round((count / total_kmers) * 100, 1) if total_kmers else 0.0
                bar_width = round((count / top_count) * 100, 1) if top_count else 0.0
                results.append(
                    {
                        "rank": rank,
                        "kmer": kmer_str,
                        "count": count,
                        "percentage": f"{pct:.1f}",
                        "bar_width": bar_width,
                    }
                )

    return render_template_string(
        HTML_TEMPLATE,
        sample_reads=sample_reads,
        selected_sample=selected_sample,
        sequence=sequence,
        k=k,
        error=error,
        results=results,
        total_kmers=total_kmers,
        unique_kmers=unique_kmers,
        top_kmer=top_kmer,
        top_count=top_count,
    )


if __name__ == "__main__":
    app.run(debug=True)
