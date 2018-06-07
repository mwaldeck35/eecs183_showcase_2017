# Dictionary of keys and a list of their corresponding notes
KEY_SIGNATURES = {
                   'c major': ['c', 'd', 'e', 'f', 'g', 'a', 'b'],
                   'c# major': ['c#', 'd#', 'f', 'f#', 'g#', 'a#', 'c'],
                   'd major': ['d', 'e', 'f#', 'g', 'a', 'b', 'c#'],
                   'eb major': ['eb', 'f', 'g', 'ab', 'bb', 'c', 'd'],
                   'e major': ['e', 'f#', 'g#', 'a', 'b', 'c#', 'd#'],
                   'f major': ['f', 'g', 'a', 'bb', 'c', 'd', 'e'],
                   'f# major': ['f#', 'g#', 'a#', 'b', 'c#', 'd#', 'f'],
                   'g major': ['g', 'a', 'b', 'c', 'd', 'e', 'f#'],
                   'ab major': ['ab', 'bb', 'c', 'db', 'eb', 'f', 'g'],
                   'a major': ['a', 'b', 'c#', 'd', 'e', 'f#', 'g#'],
                   'bb major': ['bb', 'c', 'd', 'eb', 'f', 'g', 'a'],
                   'b major': ['b', 'c#', 'd#', 'e', 'f#', 'g#', 'a#'],
                   'c minor': ['c', 'd', 'eb', 'f', 'g', 'ab', 'bb'],
                   'c# minor': ['c#', 'd#', 'e', 'f#', 'g#', 'a', 'b'],
                   'd minor': ['d', 'e', 'f', 'g', 'a', 'bb', 'c'],
                   'eb minor': ['eb', 'f', 'gb', 'ab', 'bb', 'b', 'db'],
                   'e minor': ['e', 'f#', 'g', 'a', 'b', 'c', 'd'],
                   'f minor': ['f', 'g', 'ab', 'bb', 'c', 'db', 'eb'],
                   'f# minor': ['f#', 'g#', 'a', 'b', 'c#', 'd', 'e'],
                   'g minor': ['g', 'a', 'bb', 'c', 'd', 'eb', 'f'],
                   'ab minor': ['ab', 'bb', 'b', 'db', 'eb', 'e', 'gb'],
                   'a minor': ['a', 'b', 'c', 'd', 'e', 'f', 'g'],
                   'bb minor': ['bb', 'c', 'db', 'eb', 'f', 'gb', 'ab'],
                   'b minor': ['b', 'c#', 'd', 'e', 'f#', 'g', 'a']
                 }

# List of PySynth note durations
NOTE_DURATIONS = [1, 2, -2, 4, -4, 8, -8, 16]

# Used to convert notes from numbers in the scale to letters
chromNotesLetter = {
    1: 'c',
    2: 'c#',
    3: 'd',
    4: 'eb',
    5: 'e',
    6: 'f',
    7: 'f#',
    8: 'g',
    9: 'ab',
    10: 'a',
    11: 'bb',
    12: 'b'
}

chromNotesNum = {
    'c': 1,
    'c#': 2,
    'd': 3,
    'eb': 4,
    'e': 5,
    'f': 6,
    'f#': 7,
    'g': 8,
    'ab': 9,
    'a': 10,
    'bb': 11,
    'b': 12
}

# the order of the chord progressions returned by chord prog
PROG_1_ORDER = ['I', 'IV', 'V']
PROG_2_ORDER = ['I', 'V', 'VI', 'IV']
PROG_3_ORDER = ['I', 'IV', 'I', 'V', 'I']
CIRC_PROG_ORDER = ['I', 'IV', 'V', 'I']
PROG_ORDERS = [PROG_1_ORDER, PROG_2_ORDER, PROG_3_ORDER, CIRC_PROG_ORDER]


# midi percussion instruments note values. only work on channel 9
PERCUSSION = {
    'bass': 'b3',
    'snare': 'd4',
    'hi hat': 'f#4'
}
