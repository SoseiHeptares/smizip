SmiZip
======

SmiZip is a compression method for short strings. It was developed in 1998 by
Roger Sayle (while at Metaphorics LLC) to compress SMILES strings, and
fully described at a Daylight Mug01 presentation in 2001:
https://www.daylight.com/meetings/mug01/Sayle/SmiZip/index.htm

This repo is an implementation Noel O'Boyle of the SmiZip algorithm in Python.
This work was presented at the 12th RDKit UGM in Mainz in Sep 2023:
https://github.com/SoseiHeptares/presentations/blob/main/2023/2023-09-12thRDKitUGM_NoelOBoyle_SmiZip.pdf

Note that the more recent 'smaz' (https://github.com/antirez/smaz) short string compression algorithm (2009) is equivalent in concept, but
favours a greedy approach over an optimal encoding.

Quick start
-----------

Install as follows::

   pip install smizip

First, let's download a set of n-grams trained on RDKit canonical SMILES from ChEMBL::

  curl https://raw.githubusercontent.com/SoseiHeptares/smizip/main/example-ngrams/rdkit.slow.json -o rdkit.slow.json

Now let's use this to compress and decompress a .smi file that contains canonical SMILES from RDKit::

  smizip    -i test.smi  -o test.smiz  -n rdkit.slow.json
  smizip -d -i test.smiz -o test.2.smi -n rdkit.slow.json

Other example sets of n-grams are available from the GitHub site (https://github.com/SoseiHeptares/smizip/tree/main/example-ngrams).
To create your own JSON file of n-grams, you can train on a dataset (``find_best_ngrams``), or modify
an existing JSON (``add_char_to_json``).

To use from Python:

.. code-block:: python

  import json
  from smizip import SmiZip

  json_file = "rdkit.slow.json"
  with open(json_file) as inp:
     ngrams = json.load(inp)['ngrams']

  zipper = SmiZip(ngrams)
  zipped = zipper.zip("c1ccccc1C(=O)Cl") # gives bytes
  unzipped = zipper.unzip(zipped)

Note
----

You should include ``\n`` (carraige-return) as a single-character n-gram if you intend to store the zipped representation in a file with lines terminated by ``\n``. Otherwise, the byte value of ``\n`` will be assigned to a multi-gram, and zipped SMILES will be generated containing ``\n``.

A similar warning goes for any SMILES termination character in a file. If you expect to store zipped SMILES that terminate in a TAB or SPACE character, you should add these characters as single-character n-grams. Otherwise the zipped representation may contain these and you won't know which TABs are terminations and which are part of the representation.
