SmiZip
======

SmiZip is a compression method for short strings. It was developed by
Roger Sayle in 1998 while at Metaphorics LLC to compress SMILES strings.

This repo is an implementation in Python of the SmiZip algorithm as
described by Roger in a presentation in 2001.

Quick start
-----------

Install as follows::

   pip install smizip

Let's compress a .smi file that originated with RDKit::

  python3 scripts/compress.py 

SMILES strings must be encoded and decoded with the same n-grams. These
are listed in a JSON file. Several JSON files are included by default but
you can create your own by training on a dataset (`find_best_ngrams.py`),
or by modifying existing ones (`add_char_to_json.py`).

Let's 

This codebase was developed by Noel O'Boyle based on the information in
that presentation.`
