# Day 04 - Web Application for Reference-Free k-mer Counting (SIG-mers)

## Overview & Purpose
In Day 03, I implemented the core computational step for **reference-free SIG-mer analysis** (for my M.Sc. rotation in Dudi Zeevi's lab at the Weizmann Institute): sliding a window of length `k` across raw DNA sequencing reads to extract and count overlapping k-mers without aligning to a reference genome.

In **Day 04**, the core k-mer counting business logic is separated into a reusable module (`kmer_logic.py`) and served through a lightweight **Flask** web interface (`app.py`). The web application allows researchers to:
- Select a sequencing read from the sample dataset (`reads.csv`) or paste any custom DNA sequence.
- Choose any k-mer window size (`k`).
- Immediately inspect summary metrics (sequence length, total overlapping k-mers, unique k-mers, and the top SIG-mer candidate) alongside a full ranked frequency table and relative distribution bars.

## Files
- `kmer_logic.py` - Core business logic copied and modularized from Day 03 (`count_kmers`, sequence validation, and CSV sample loading). Can also be run standalone from the command line.
- `app.py` - Flask web application providing an interactive HTML form and results table.
- `reads.csv` - Sample dataset of short DNA sequencing reads (`read_id`, `dna_sequence`).
- `requirements.txt` - Python package dependencies (`Flask`).

## Installation & Running Locally

1. Navigate to the `day04` folder:
   ```bash
   cd day04
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Run the standalone logic (optional verification):
   ```bash
   python kmer_logic.py
   ```

4. Launch the Flask web application:
   ```bash
   python app.py
   ```
   Then open `http://127.0.0.1:5000` in your browser.

## AI Prompts Used
> Act as an expert Python software engineer and autonomous GitHub agent. I need to complete the "Day 04" assignment for my Weizmann Python course.
>
> Assignment Objective:
> Take the "business logic" from Day 03 (reference-free k-mer counting for SIG-mers), copy it to a new 'day04' folder, and build a lightweight web application using Flask with a clean, functional web interface.
>
> Here is the exact workflow you must execute across the two repositories:
>
> 1. MY ASSIGNMENTS REPOSITORY (Local workspace):
> - Create a new directory named 'day04'.
> - Copy the core calculation logic from 'day03' into 'day04' (e.g., 'kmer_logic.py') ensuring the original Day 03 code remains completely intact.
> - Create a Flask web application ('app.py'):
>   - Set up a clean HTML form (either embedded in a templates folder or inline using render_template_string) where a user can enter a DNA sequence and a value for k (or select from sample reads).
>   - When submitted, call the k-mer counting function and display the results (top k-mers / SIG-mer candidates and their counts) directly on the web page.
> - Add a 'requirements.txt' containing 'Flask'.
> - Verify that both the standalone logic and the Flask application run without errors.
> - Create 'day04/README.md':
>   - Explain the purpose of the web interface and how it serves the k-mer counting logic.
>   - Provide instructions on how to install dependencies and run the Flask app locally ('python app.py').
>   - Document the AI prompts used.
> - Commit all changes and push them to 'main' on my personal remote repository (origin).
>
> 2. THE COURSE REPOSITORY (wis-python-course-2026-10):
> - Using GitHub CLI (`gh issue create`) or the GitHub API:
> - Create a new issue titled: "Day 04 by Elad Cohen"
> - In the body of the issue, provide the direct link to the 'day04' folder inside my personal assignments repository.
