#!/usr/bin/python

import sys
from copy import copy

class Note:
    _NOTES = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B']
    _NOTE_TO_VALUE = dict(zip(_NOTES, range(len(_NOTES))))
    _OFFSET = { 'b': -1, '#': 1 }

    def __init__(self, string=None, value=None):
        if string is not None:
            value = self._string_to_value(string)
        if value is None:
            raise RuntimeError('value is required')
        self.value = value

    def cannonical_value(self):
        return self.value % len(self._NOTES)

    def __iadd__(self, other):
       self.value += other
       return self

    def __isub__(self, other):
       self.value -= other
       return self

    def __repr__(self):
        return str(self)

    def __str__(self):
        return self._NOTES[self.cannonical_value()]

    def __add__(self, other):
        return Note(value=self.value + other)

    @staticmethod
    def _string_to_value(note):
        offset = 0
        if len(note) > 1:
            offset = Note._OFFSET[note[-1]]
            note = note[:-1]
        return Note._NOTE_TO_VALUE[note] + offset

class ScaleGenerator:
    def __init__(self, note):
        self.note = copy(note)
        self._iter = iter(self.INCREMENTS)

    def __iter__(self):
        return self

    def __next__(self):
        increment = next(self._iter)
        self.note += increment
        return copy(self.note)

    @staticmethod
    def from_string(string):
        key = string[0]
        note = Note(string[1:])
        if key == 'M':
            return MajorScaleGenerator(note)
        elif key == 'm':
            return MinorScaleGenerator(note)
        else:
            raise RuntimeError('Invalid spec for scale')


class MajorScaleGenerator(ScaleGenerator):
    INCREMENTS=[0, 2, 2, 1, 2, 2, 2]

class MinorScaleGenerator(ScaleGenerator):
    INCREMENTS=[0, 2, 1, 2, 2, 1, 2]


class Scale:
    _SCALES = 'MA MA# MB MC MC# MD MD# ME MF MF# MG MG# mA mA# mB mC mC# mD mD# mE mF mF# mG mG#'.split(' ')
    _DISTINCT_SCALES=None

    def __init__(self, name):
        self.name  = name
        self.notes = [note for note in ScaleGenerator.from_string(name)]
        self.cannonical_note_set = set(str(note) for note in self.notes)

    def includes(self, cannonical_notes):
        # print('[%s] is superset %s of %s' % (self.name, self.cannonical_note_set, notes))
        return self.cannonical_note_set.issuperset(cannonical_notes)

    @staticmethod
    def distinct_scales():
        if Scale._DISTINCT_SCALES is None:
            Scale._DISTINCT_SCALES = [Scale(name) for name in Scale._SCALES]
        return Scale._DISTINCT_SCALES

class Case:
    def __init__(self, number_of_case, notes):
        self.number_of_case = number_of_case
        self.cannonical_notes = set(str(Note(note)) for note in notes)

    def scales(self):
        all_scales = Scale.distinct_scales()
        if len(self.cannonical_notes) == 0:
            included_scales = all_scales
        else:
            included_scales = list(filter(lambda scale: scale.includes(self.cannonical_notes), all_scales))
        if len(included_scales) == 0:
            return "None"
        else:
            return ' '.join(map(lambda scale: scale.name, included_scales))

class CasesIterator:
    def __init__(self):
        self._iter = iter(sys.stdin)
        self.number_of_cases = next(self._iter).rstrip()
        self.current_case = 0

    def __iter__(self):
        return self

    def __next__(self):
        number_of_notes = int(next(self._iter).rstrip())
        if number_of_notes > 0:
            notes = set(next(self._iter).rstrip().split(' '))
        else:
            notes = []
        self.current_case+=1
        return Case(self.current_case, notes)

for case in CasesIterator():
    print("Case #%d: %s" % (case.number_of_case, case.scales()))
