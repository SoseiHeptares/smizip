"""Tests."""

from smizip import SmiZip
import unittest


class TestZip(unittest.TestCase):
    """Test zipping."""

    def test_fail_load(self):
        """Test a round trip."""
        with self.assertRaises(ValueError):
            SmiZip.load("nope")

    def test_zip(self):
        """Test a round trip."""
        zipper = SmiZip.load("rdkit.slow")
        smiles = "c1ccccc1C(=O)Cl"
        zipped = zipper.zip(smiles)
        self.assertIsInstance(zipped, bytes)
        unzipped = zipper.unzip(zipped)
        self.assertEqual(smiles, unzipped)
