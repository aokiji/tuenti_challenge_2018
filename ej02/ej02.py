#!/usr/bin/python

import sys

class MaximumValueIterator:
    def __init__(self, case):
        self._iter = iter(case.secret_string)
        self.assigned_values = {}
        self.last_assigned_value = case.base

    def __iter__(self):
        return self

    def __next__(self):
        char = next(self._iter)
        if char in self.assigned_values:
            return self.assigned_values[char]
        else:
            self.last_assigned_value-=1
            self.assigned_values[char] = self.last_assigned_value
            return self.last_assigned_value

class MinimumValueIterator:
    def __init__(self, case):
        self._iter = iter(case.secret_string)
        self.assigned_values = {}
        self.last_assigned_value = 0

    def __iter__(self):
        return self

    def __next__(self):
        char = next(self._iter)
        if char in self.assigned_values:
            return self.assigned_values[char]
        else:
            if self.last_assigned_value == 1:
                value = 0
            elif self.last_assigned_value == 0:
                value = 1
            else:
                value = self.last_assigned_value
            self.last_assigned_value+=1
            self.assigned_values[char] = value
            return value

class Case:
    def __init__(self, number_of_case, secret_string):
        self.secret_string = secret_string
        self.number_of_case = number_of_case
        self.base = len(set(secret_string))

    def difference(self):
        maximum_value = MaximumValueIterator(self)
        minimum_value = MinimumValueIterator(self)

        difference = 0
        for num_char, char in enumerate(self.secret_string):
            exp = len(self.secret_string) - num_char - 1
            difference += (next(maximum_value) - next(minimum_value)) * self.base**exp

        return difference

class CasesIterator:
    def __init__(self):
        self._iter = iter(sys.stdin)
        self.number_of_cases = next(self._iter).rstrip()
        self.current_case = 0

    def __iter__(self):
        return self

    def __next__(self):
        next_line = next(self._iter).rstrip()
        self.current_case+=1
        return Case(self.current_case, next_line)

for case in CasesIterator():
    print("Case #%d: %d" % (case.number_of_case, case.difference()))
