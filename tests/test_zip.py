"""Tests."""

import json

from smizip import SmiZip
from smizip.smizip import EXAMPLES
import unittest


class TestZip(unittest.TestCase):
    """Test zipping."""

    def test_fail_load(self):
        """Test a round trip."""
        with self.assertRaises(ValueError):
            SmiZip.load("nope")

    def test_load_builtin(self):
        """Test loading from a builtin object."""
        zipper = SmiZip.load("rdkit.slow")
        self.assert_roundtrips(zipper)

    def test_load_path(self):
        """Test loading from a specific file path."""
        path = EXAMPLES.joinpath("ob.slow.json")
        zipper = SmiZip.load(path)
        self.assert_roundtrips(zipper)

    def test_load_multigrams(self):
        """Test loading from a specific file path."""
        path = EXAMPLES.joinpath("ob.slow.json")
        multigrams = json.loads(path.read_text())["ngrams"]
        zipper = SmiZip(multigrams)
        self.assert_roundtrips(zipper)

    def assert_roundtrips(self, zipper: SmiZip):
        """Test that a molecule can be round-tripped."""
        smiles = "c1ccccc1C(=O)Cl"
        zipped = zipper.zip(smiles)
        self.assertIsInstance(zipped, bytes)
        unzipped = zipper.unzip(zipped)
        self.assertEqual(smiles, unzipped)
