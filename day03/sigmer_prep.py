"""Preliminary step for SIG-mer analysis: k-mer extraction and counting."""
import csv
from collections import Counter

K = 4


def count_kmers(sequence, k=K):
    """Return a Counter of all overlapping k-mers in a DNA sequence."""
    sequence = sequence.strip().upper()
    return Counter(sequence[i:i + k] for i in range(len(sequence) - k + 1))


def main(path="reads.csv", k=K):
    with open(path, newline="") as f:
        for row in csv.DictReader(f):
            counts = count_kmers(row["dna_sequence"], k)
            kmer, n = counts.most_common(1)[0]
            print(f"{row['read_id']}: most frequent {k}-mer = {kmer} ({n} times)")


if __name__ == "__main__":
    main()
