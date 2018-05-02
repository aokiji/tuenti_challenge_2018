#!/usr/bin/python

import sys

class Case:
    def __init__(self, number_of_case, vertical_lines, horizontal_lines):
        self.vertical_lines = vertical_lines
        self.horizontal_lines = horizontal_lines
        self.number_of_case = number_of_case

    def number_of_holes(self):
        return (self.vertical_lines - 1)*(self.horizontal_lines - 1)

class CasesIterator:
    def __init__(self):
        self._iter = iter(sys.stdin)
        self.number_of_cases = next(self._iter).rstrip()
        self.current_case = 0

    def __iter__(self):
        return self

    def __next__(self):
        next_line = next(self._iter).rstrip()
        return self._parse(next_line)

    def _parse(self, next_line):
        (vertical_lines, horizontal_lines) = next_line.split(' ')
        self.current_case+=1
        return Case(self.current_case, int(vertical_lines), int(horizontal_lines))

for case in CasesIterator():
    print("Case #%d: %d" % (case.number_of_case, case.number_of_holes()))
