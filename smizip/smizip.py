import sys
import time
from typing import List
import collections
import ahocorasick

class SmiZip():
    def __init__(self, multigrams: List[str]) -> None:
        """Requires a list of N multigrams (N<=256) corresponding to bytes 0->N"""

        if len(multigrams) > 256:
            raise RuntimeError(f"The number of multigrams provided was {len(multigrams)} but should be <= 256")

        self.multigrams = multigrams

        self.lookup = {}
        self.singlechars = set()
        self.multichars = []
        for idx, multigram in enumerate(multigrams):
            self.lookup[multigram] = idx
            if len(multigram) == 1:
                self.singlechars.add(multigram)
            else:
                self.multichars.append(multigram)

        self.auto = None

    def unzip(self, text: str):
        ans = []
        for letter in text:
            ans.append(self.multigrams[letter])
        return "".join(ans)

    def zip(self, text: str, format=0):
        if self.auto is None and self.multichars:
            self.auto = ahocorasick.Automaton()
            for multichar in self.multichars:
                self.auto.add_word(multichar, multichar)
            self.auto.make_automaton()

        matches = [] if self.auto is None else list(self.auto.iter(text)) # [(endidx, string), ...]

        matches_by_endidx = collections.defaultdict(list)
        for endidx, ngram in matches:
            matches_by_endidx[endidx].append(ngram)

        solution = [0] # the min number of multigrams for the substring of length idx
        chosen = []
        N = len(text)
        for i in range(N):
            all_data = []
            all_data.append( (solution[i], text[i]) ) # handle single-char
            for ngram in matches_by_endidx[i]:
                ngram_len = len(ngram)
                data = (solution[i-ngram_len+1], ngram)
                all_data.append(data)
            all_data.sort()
            solution.append(all_data[0][0] + 1)
            chosen.append(all_data[0][1])

        # We have the best length
        # ...we just need to backtrack to find the multigrams that were chosen
        i = len(text) - 1
        multigrams = []
        while i >= 0:
            multigram = chosen[i]
            multigrams.append(multigram)
            i -= len(multigram)
        multigrams.reverse()
        if format == 0:
            return bytes(self.lookup[multigram] for multigram in multigrams)
        elif format == 1:
            return multigrams
        else:
            return [self.lookup[multigram] for multigram in multigrams]
