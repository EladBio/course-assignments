# Day 03 - k-mer extraction and counting (SIG-mers preparation)

## Biological context
I am an M.Sc. student in Systems and Computational Biology at the Weizmann Institute, starting a rotation in Dudi Zeevi's lab. My project will focus on **reference-free SIG-mers**, i.e. working with short sequence words (k-mers) taken directly from raw sequencing reads, without aligning to a reference genome. A basic first step is extracting k-mers from reads and counting how often each appears. This assignment implements that step.

## Files
- `reads.csv` - mock dataset of short DNA reads (`read_id`, `dna_sequence`).
- `sigmer_prep.py` - the code.

## What the code does
- `count_kmers(sequence, k=4)` slides a window of length `k` over the sequence, extracts every overlapping k-mer, and returns a `Counter` of frequencies.
- The script reads `reads.csv`, applies the function to every read and prints the most frequent k-mer of each read.

Run: `python sigmer_prep.py`

## Prompts used
> Act as an expert Python programmer and bioinformatics assistant. I need to complete a "Day 03" assignment for my Python course. The assignment requires creating a Python script with a specific function, reading input data from an external file, and documenting the process. I am an M.Sc. student at the Weizmann Institute about to do a rotation in Dudi Zeevi's lab on reference-free SIG-mers. Generate reads.csv (read_id, dna_sequence), sigmer_prep.py (a count_kmers function with k=4, reading the CSV and printing the most frequent k-mer per read), and a README.md.
