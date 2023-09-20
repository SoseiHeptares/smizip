SmiZip
======

SmiZip is a compression method for short strings. It was developed by
Roger Sayle in 1998 while at Metaphorics LLC to compress SMILES strings.

This repo is an implementation in Python by Noel O'Boyle of the SmiZip algorithm as
described by Roger in a Mug01 presentation in 2001:
https://www.daylight.com/meetings/mug01/Sayle/SmiZip/index.htm

Quick start
-----------

Install as follows::

   pip install smizip

Let's compress and decompress a .smi file that contains canonical SMILES from RDKit
using n-grams trained for this purpose listed in `rdkit.slow.json` (available from
the GitHub site)::

  smizip    -i test.smi  -o test.smiz  -n example-ngrams/rdkit.slow.json
  smizip -d -i test.smiz -o test.2.smi -n example-ngrams/rdkit.slow.json

To create your own JSON file of n-grams, you can train on a dataset (`find_best_ngrams.py`),
or modify an existing JSON (`add_char_to_json.py`).

To use from Python::

  import json
  from smizip import SmiZip

  json_file = "rdkit.slow.json"
  with open(json_file) as inp:
     ngrams = json.load(inp)

  zipper = SmiZip(ngrams)
  zipped = zipper.zip("c1ccccc1C(=O)Cl") # gives bytes
  unzipped = zipper.unzip(zipped)

Note
----

You should include "\n" (carraige-return) as a single-character n-gram if you intend to store the zipped representation in a file with lines terminated by "\n". Otherwise, the byte value of "\n" will be assigned to a multi-gram, and zipped SMILES will be generated containing "\n".

A similar warning goes for any SMILES termination character in a file. If you expect to store zipped SMILES that terminate in a TAB or SPACE character, you should add these characters as single-character n-grams. Otherwise the zipped representation may contain these and you won't know which TABs are terminations and which are part of the representation.
