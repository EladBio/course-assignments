"""Core business logic for reference-free k-mer extraction and counting (SIG-mer preparation)."""
import csv
from collections import Counter
from pathlib import Path

K = 4
READS_CSV_PATH = Path(__file__).resolve().parent / "reads.csv"
VALID_BASES = set("ACGTN")


def clean_sequence(sequence: str) -> str:
    """Normalize a raw DNA sequence string by stripping whitespace and uppercasing."""
    return "".join(sequence.split()).upper()


def validate_sequence(sequence: str, k: int = K) -> tuple[bool, str]:
    """Validate that a DNA sequence and k value are suitable for k-mer counting."""
    seq = clean_sequence(sequence)
    if not seq:
        return False, "Please enter a DNA sequence or select a sample read."
    invalid_chars = sorted(set(seq) - VALID_BASES)
    if invalid_chars:
        return False, f"Invalid nucleotide character(s) found: {', '.join(invalid_chars)}. Allowed: A, C, G, T, N."
    if k < 1:
        return False, "k must be a positive integer (at least 1)."
    if len(seq) < k:
        return False, f"Sequence length ({len(seq)} bp) must be at least k ({k})."
    return True, ""


def count_kmers(sequence: str, k: int = K) -> Counter:
    """Return a Counter of all overlapping k-mers in a DNA sequence."""
    sequence = clean_sequence(sequence)
    if k < 1 or len(sequence) < k:
        return Counter()
    return Counter(sequence[i:i + k] for i in range(len(sequence) - k + 1))


def load_sample_reads(path: str | Path = READS_CSV_PATH) -> dict[str, str]:
    """Load sample DNA reads from reads.csv as a dictionary mapping read_id -> dna_sequence."""
    csv_path = Path(path)
    if not csv_path.is_absolute() and not csv_path.exists():
        csv_path = READS_CSV_PATH
    reads: dict[str, str] = {}
    with open(csv_path, newline="") as f:
        for row in csv.DictReader(f):
            reads[row["read_id"].strip()] = clean_sequence(row["dna_sequence"])
    return reads


def main(path: str | Path = READS_CSV_PATH, k: int = K) -> None:
    """Run standalone k-mer counting on all sample reads in reads.csv."""
    for read_id, sequence in load_sample_reads(path).items():
        counts = count_kmers(sequence, k)
        kmer, n = counts.most_common(1)[0]
        print(f"{read_id}: most frequent {k}-mer = {kmer} ({n} times)")


if __name__ == "__main__":
    main()
