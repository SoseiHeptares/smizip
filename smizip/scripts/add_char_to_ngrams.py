import sys
import json
import argparse

from . import find_best_ngrams as fbn

def parse_args():
    parser = argparse.ArgumentParser(description="Find a set of ngrams that maximally compresses a training set")
    parser.add_argument("-i", "--input", help="Input JSON file", required=True)
    parser.add_argument("-o", "--output", help="Output JSON file", required=True)
    parser.add_argument("-c", "--chars", help="Add these characters to the list of n-grams", default=[])
    parser.add_argument("--zero", action="store_true", help="Include \\0 as an n-gram")
    parser.add_argument("--tab", action="store_true", help="Include TAB as an n-gram")
    parser.add_argument("--space", action="store_true", help="Include SPACE as an n-gram")
    parser.add_argument("--cr", action="store_true", help="Include \\n (carraige-return) as an n-gram")
    args = parser.parse_args()
    return args

def main():
    args = parse_args()

    with open(args.input) as inp:
        details = json.load(inp)

    extrachars = set(args.chars)
    if args.cr:
        extrachars.add("\n")
    if args.tab:
        extrachars.add("\t")
    if args.space:
        extrachars.add(" ")
    if args.zero:
        extrachars.add("\0")

    for char in extrachars:
        if char in details['metadata']['initial_chars']:
            sys.exit(f"ERROR: Character '{char}' already listed in the initial_chars field in the metadata")
        if char in details['ngrams']:
            sys.exit(f"ERROR: Character '{char}' already present as one of the n-grams")

    singlechars = "".join(sorted(x for x in details['ngrams'] if len(x) == 1) + list(extrachars))
    multichars = [x for x in details['ngrams'] if len(x) > 1]
    multichars = multichars[:256-len(singlechars)]
    assert len(singlechars) + len(multichars) == 256
    encoding = fbn.create_encoding(singlechars, multichars)

    details['ngrams'] = encoding
    details['metadata']['initial_chars'] = singlechars

    with open(args.output, "w") as out:
        json.dump(details, out)

if __name__ == "__main__":
    main()

