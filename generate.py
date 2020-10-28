#!/usr/bin/env python/Users/matt_waldeck/desktop
import sys
sys.dont_write_bytecode = True # Suppress .pyc files

import random
import chart_studio.plotly as py
import numpy as np
import midi
from pysynth import pysynth
from data.dataLoader import *
from models.musicInfo import *
from models.unigramModel import *
from models.bigramModel import *
from models.trigramModel import *
from plotly.graph_objs import *
from plotly.tools import FigureFactory as FF

TEAM = 'Musical Jelly Beans'
LYRICSDIRS = ['the_beatles']
MUSICDIRS = ['gamecube']
WAVDIR = 'wav/'

###############################################################################
# Helper Functions
###############################################################################

def sentenceTooLong(desiredLength, currentLength):
    """
    Requires: nothing
    Modifies: nothing
    Effects:  returns a bool indicating whether or not this sentence should
              be ended based on its length. This function has been done for
              you.
    """
    STDEV = 1
    val = random.gauss(currentLength, STDEV)
    return val > desiredLength

def printSongLyrics(verseOne, verseTwo, chorus):
    """
    Requires: verseOne, verseTwo, and chorus are lists of lists of strings
    Modifies: nothing
    Effects:  prints the song. This function is done for you.
    """
    verses = [verseOne, chorus, verseTwo, chorus]
    print
    for verse in verses:
        for line in verse:
            print (' '.join(line)).capitalize()
        print

def trainLyricModels(lyricDirs):
    """
    Requires: lyricDirs is a list of directories in data/lyrics/
    Modifies: nothing
    Effects:  loads data from the folders in the lyricDirs list,
              using the pre-written DataLoader class, then creates an
              instance of each of the NGramModel child classes and trains
              them using the text loaded from the data loader. The list
              should be in tri-, then bi-, then unigramModel order.

              Returns the list of trained models.
    """
    models = [TrigramModel(), BigramModel(), UnigramModel()]
    for ldir in lyricDirs:
        lyrics = loadLyrics(ldir)
        for model in models:
            model.trainModel(lyrics)
    return models

###############################################################################
# Core
###############################################################################

def trainMusicModels(musicDirs):
    """
    Requires: lyricDirs is a list of directories in data/midi/
    Modifies: nothing

    Effects:  works exactly as trainLyricsModels, except that
              now the dataLoader calls the DataLoader's loadMusic() function
              and takes a music directory name instead of an artist name.
              Returns a list of trained models in order of tri-, then bi-, then
              unigramModel objects.
    """
    models = [TrigramModel(), BigramModel(), UnigramModel()]
    for musicDir in musicDirs:
        music = loadMusic(musicDir)
        for model in models:
            model.trainModel(music)
    return models

def selectNGramModel(models, sentence):
    """
    Requires: models is a list of NGramModel objects sorted by descending
              priority: tri-, then bi-, then unigrams.
    Modifies: nothing
    Effects:  returns the best possible model that can be used for the
              current sentence based on the n-grams that the models know.
              (Remember that you wrote a function that checks if a model can
              be used to pick a word for a sentence!)
    """

    for m in models:
        if m.trainingDataHasNGram(sentence):
            return m
    return models[2]


def generateLyricalSentence(models, desiredLength):
    """
    Requires: models is a list of trained NGramModel objects sorted by
              descending priority: tri-, then bi-, then unigrams.
              desiredLength is the desired length of the sentence.
    Modifies: nothing
    Effects:  returns a list of strings where each string is a word in the
              generated sentence. The returned list should NOT include
              any of the special starting or ending symbols.

              For more details about generating a sentence using the
              NGramModels, see the spec.
    """
    sentence = ['^::^', '^:::^']
    model = selectNGramModel(models, sentence)
    nextToken = model.getNextToken(sentence)
    while (not sentenceTooLong(desiredLength, len(sentence)-2)) and nextToken != "$:::$":
        sentence.append(nextToken)
        model = selectNGramModel(models, sentence)
        nextToken = model.getNextToken(sentence)
    return sentence[2:]

def generateMusicalSentence(models, desiredLength, possiblePitches):
    """
    Requires: possiblePitches is a list of pitches for a musical key
    Modifies: nothing
    Effects:  works exactly like generateLyricalSentence from the core, except
              now we call the NGramModel child class' getNextNote()
              function instead of getNextToken(). Everything else
              should be exactly the same as the core.
    """
    sentence = ['^::^', '^:::^']
    model = selectNGramModel(models, sentence)
    nextNote = model.getNextNote(sentence, possiblePitches)
    # nextNote = selectNGramModel(models, sentence).getNextNote(sentence,
    #                                                          possiblePitches))
    while (not sentenceTooLong(desiredLength, len(sentence)-2)) and nextNote != "$:::$":
        sentence.append(nextNote)
        model = selectNGramModel(models, sentence)
        nextNote = model.getNextNote(sentence, possiblePitches)

    return sentence[2:]

def runLyricsGenerator(models):
    """
    Requires: models is a list of a trained nGramModel child class objects
    Modifies: nothing
    Effects:  generates a verse one, a verse two, and a chorus, then
              calls printSongLyrics to print the song out.
    """
    verseOne = []
    verseTwo = []
    chorus = []
    lengths = 8
    for i in range(4):
        verseOne.append(generateLyricalSentence(models, lengths))
        verseTwo.append(generateLyricalSentence(models, lengths))
        chorus.append(generateLyricalSentence(models, lengths))

    printSongLyrics(verseOne, verseTwo, chorus)

def runMusicGenerator(models, songName):
    """
    Requires: models is a list of trained models
    Modifies: nothing
    Effects:  runs the music generator as following the details in the spec.
    """
    key = random.choice(KEY_SIGNATURES.keys())
    possiblePitches = KEY_SIGNATURES[key]
    desiredLength = 100
    line = generateMusicalSentence(models, desiredLength, possiblePitches)
    pysynth.make_wav(line, fn=songName)

###############################################################################
# Reach
###############################################################################

def createMajorChord(n):
    # n is the number of the note as listed in the kyes of chromNotesLetter
    chord = []
    if n <= 12:
        #converts the number pitch back into letter notation
        chord.append(chromNotesLetter[n])
    else:
        #prevents the pitch number from going out of the pitch range
        n = n - 12
        chord.append(chromNotesLetter[n])
    n += 4
    if n <= 12:
        chord.append(chromNotesLetter[n])
    else:
        n = n - 12
        chord.append(chromNotesLetter[n])
    n += 3
    if n <= 12:
        chord.append(chromNotesLetter[n])
    else:
        n = n - 12
        chord.append(chromNotesLetter[n])
    return chord

def createMinorChord(n):
    chord = []
    #couldnt use for loop because the distance between notes is different
    if n <= 12:
        chord.append(chromNotesLetter[n])
    else:
        n = n - 12
        chord.append(chromNotesLetter[n])
    # the distance between the first note and the second note is 3 half steps
    n += 3
    if n <= 12:
        chord.append(chromNotesLetter[n])
    else:
        n -= 12
        chord.append(chromNotesLetter[n])
    # the distance between the second note and the third note in the scale is 4 half steps
    n += 4
    if n <= 12:
        chord.append(chromNotesLetter[n])
    else:
        n -= 12
        chord.append(chromNotesLetter[n])
    return chord

def chordProg(key):
    x = ''
    if key in KEY_SIGNATURES:
        if 'major' in key:
            startNote = KEY_SIGNATURES[key][0]
            #turns the letter note into number note, so it can be used to add one (half step) to change the pitch
            x = chromNotesNum[startNote]
            #example for progression using c major key
            # createMajorChord(x) would be createMajorChord(1) and will return a c major triad chord containting [c, e, g]
            # createMajorChord(x + 5) which would be createMajorChord(6) will return a f major triad chord that contains [f, a, c]
            # etc.
            prog1 = {'I': createMajorChord(x),
                     'IV': createMajorChord(x + 5),
                     'V': createMajorChord(x + 7)}
            prog2 = {'I': createMajorChord(x),
                     'V': createMajorChord(x + 7),
                     'VI':  createMajorChord(x + 9),
                     'IV': createMajorChord(x + 5)}
            prog3 = {'I': createMajorChord(x),
                     'IV': createMajorChord(x + 5),
                     'I': createMajorChord(x),
                     'V': createMajorChord(x + 7),
                     'I': createMajorChord(x)}
            circProg = {'I': createMajorChord(x),
                        'IV': createMajorChord(x + 5),
                        'V': createMajorChord(x + 7)}
            return [prog1, prog2, prog3, circProg]
        if 'minor' in key:
            startNote = KEY_SIGNATURES[key][0]
            x = chromNotesNum[startNote]
            mprog1 = {'I': createMinorChord(x),
                      'IV': createMinorChord(x + 5),
                      'V': createMajorChord(x + 7)}
            mprog2 = {'I': createMinorChord(x),
                      'V': createMajorChord(x + 7),
                      'VI':  createMajorChord(x + 9),
                      'IV': createMinorChord(x + 5)}
            mprog3 = {'I': createMinorChord(x),
                      'IV': createMinorChord(x + 5),
                      'I': createMinorChord(x),
                      'V': createMajorChord(x + 7),
                      'I': createMinorChord(x)}
            mcircProg = {'I': createMinorChord(x),
                         'IV': createMinorChord(x + 5),
                         'V': createMajorChord(x + 7)}
            return [mprog1, mprog2, mprog3, mcircProg]
    else:
        print 'not valid key signature'
        return


def durationToBeats(duration):
    halfNoteModifier = 1
    if duration < 0:
        halfNoteModifier = 1.5
        duration *= -1
    return (4.0 / duration) * halfNoteModifier

def beatsToDuration(beats):
    duration = 4.0 / beats
    if duration % 1 == 0:
        return int(duration)
    else:
        return int(4.0 / (beats / 1.5)) * -1

def limitPhraseLength(phrase, desiredLength):
    '''
    phrase is a list of pysynth tuples
    desiredLength is the number of beats to limit phrase to
    directly modifies phrase
    '''
    # absoluteTime and noteEnds are in beats
    absoluteTime = 0
    noteEnds = []
    for note in phrase:
        noteLength = durationToBeats(note[1])
        noteEnds.append(absoluteTime + noteLength)
        absoluteTime += noteLength
    # indexing in reverse order to avoid problems with popping
    for i in range(len(noteEnds)-1, -1, -1):
        if noteEnds[i] > desiredLength:
            oldNote = phrase[i]
            oldNoteLength = durationToBeats(oldNote[1])
            overflow = noteEnds[i] - desiredLength
            newNoteLength = oldNoteLength - overflow
            if newNoteLength <= 0:
                # means the note started after the desiredLength
                phrase.pop(i)
            else:
                phrase[i] = (oldNote[0], beatsToDuration(newNoteLength))

def repeatPhrase(phrase, repetitions):
    '''
    modifies phrase, which is a list of pysynth tuples
    repetitions is the number of times to repeat the phrase
    '''
    # copies the value of phrase, not just the reference
    initialPhrase = list(phrase)
    for _ in range(repetitions):
        phrase.extend(initialPhrase)

def makeBoosted(phrase):
    # USED FOR PYSYNTH. NOT USED ANYMORE
    '''
    modifies phrase, which is a list of pysynth tuples. Adds asterisks to
    every note
    '''
    for i in range(len(phrase)):
        phrase[i] = (phrase[i][0] + '*', phrase[i][1])

def addChordsToSong(song, key, progNum, beats, octave):
    '''
    modifies song, which is a list of lists of pysynth tuples. adds three lists,
        one for each part of the chord
    key is a key from KEY_SIGNATURES
    progNum is an index from PROG_ORDERS
    beats is the number of beats per chord as an int
    octave is the octave of the chords as an int
    '''
    duration = beatsToDuration(beats)
    chordProgs = chordProg(key)
    chords = []
    for root in PROG_ORDERS[progNum]:
        chords.append(chordProgs[progNum][root])
    for chordPart in range(3):
        chordParts = []
        for chord in chords:
            note = chord[chordPart] + str(octave)
            chordParts.append((note, duration))
        song.append(chordParts)

def addBassToSong(song, key, progNum, beats, octave, noteDurations):
    '''
    modifies song, which is a list of lists of pysynth tuples. adds one list
        for the bass line
    key is a key from KEY_SIGNATURES
    progNum is an index from PROG_ORDERS
    beats is the number of beats per chord as an int
    octave is the octave of the chords as an int
    noteDurations is a list of possible pysynth note durations for the bass line
    '''
    chordProgs = chordProg(key)
    chords = []
    for root in PROG_ORDERS[progNum]:
        chords.append(chordProgs[progNum][root])
    track = []
    for chord in chords:
        phrase = []
        # 16th notes are the shortest note length
        for _ in range(4*beats):
            note = random.choice(chord) + str(octave)
            phrase.append((note, random.choice(noteDurations)))
        limitPhraseLength(phrase, beats)
        track.extend(phrase)
    song.append(track)

def addMelodyToSong(models, song, key, progNum, beatsPerChord, progReps,
                    octave):
    '''
    models is a list of trained music models
    modifies song, a list of lists of pysynth tuples
    key is a key from KEY_SIGNATURES
    progNum is an index of PROG_ORDERS
    progReps is an int of the number of times the progression loops
    numChords is an int
    beats is desired lengtho fo the melody
    octave is the octave to restrict the notes to
    '''
    chordProgs = chordProg(key)
    chords = []
    for root in PROG_ORDERS[progNum]:
        chords.append(chordProgs[progNum][root])
    melody = []
    for _ in range(progReps):
        for chord in chords:
            phrase = generateMusicalSentence(models, beatsPerChord * 5, chord)
            limitPhraseLength(phrase, beatsPerChord)
            melody.extend(phrase)
    # restrict melody's octave
    for i in range(len(melody)):
        oldOctave = int(melody[i][0][-1])
        if oldOctave != octave:
            pitch = melody[i][0][:-1]
            melody[i] = (pitch + str(octave), melody[i][1])
    song.append(melody)

def addPercussionToSong(song, instruments, beats, reps):
    '''
    modifies song, which is a list of lists of pysynth tuples
    instruments is a list of notes corresponding to percussion instruments as
        specified in musicInfo
    beats is an int; the length of the percussion phrase
    reps is an int; the number of times to repeat the phrase
    '''
    phrase = []
    for _ in range(beats * 4):
        phrase.append((random.choice(instruments),
                       random.choice(NOTE_DURATIONS[3:])))
    limitPhraseLength(phrase, beats)
    repeatPhrase(phrase, reps - 1)
    song.append(phrase)

def makeSongPySynth(song, instruments, volume, name, bpm):
    # ONLY WORKS WITH <= 3 TRACKS. NOT USED ANYMORE
    '''
    song is a list of lists of pysynth tuples
    instruments is a list of pysynth versions to use to make each track
    volume is a list of floats that specifies the boosted value for each track
    name is the name to save the song as, not a path, no file extension
    bpm is an int
    '''
    trackNums = list(range(len(song)))
    # make individual tracks
    for i in trackNums:
        tempPath = 'wav/temp/' + str(i) + '+.wav'
        instruments[i].make_wav(song[i], bpm, fn=tempPath, boost=volume[i])
    # mix tracks together
    songPath = 'wav/' + name + '.wav'
    for i in trackNums[1:]:
        prevComboPath = 'wav/temp/'
        for j in trackNums[:i]:
            prevComboPath += str(j) + '+'
        newComboPath = prevComboPath + str(i) + '+.wav'
        prevComboPath += '.wav'
        tempPath = 'wav/temp/' + str(i) + '+.wav'
        if not i == trackNums[-1]:
            pysynth.mix_files(prevComboPath, tempPath, newComboPath)
        else:
            pysynth.mix_files(prevComboPath, tempPath, songPath)

def makeSongMidi(song, instruments, volume, name, bpm):
    '''
    song is a list of lists of pysynth tuples
    instruments is a list of ints specifying midi instruments; -1 means to use
        channel 9 to produce percussion sounds
    volume is a list of ints specifying the volume of each track
    name is the song's name
    '''
    # 220 is completely arbitrary. anything >= 4 should probably work
    resolution = 1000
    pattern = midi.Pattern(resolution=resolution)

    tempoEvent = midi.SetTempoEvent(tick=0)
    tempoEvent.set_bpm(bpm)
    tempoTrack = midi.Track()
    tempoTrack.append(tempoEvent)
    tempoTrack.append(midi.EndOfTrackEvent(tick=0))
    pattern.append(tempoTrack)

    for i in range(len(song)):
        track = midi.Track()
        if instruments[i] != -1:
            track.append(midi.ProgramChangeEvent(tick=0, channel=i,
                                             data=[instruments[i]]))
        for note in song[i]:
            noteLetter = note[0][:-1]
            noteNum = chromNotesNum[noteLetter] - 1
            octave = int(note[0][-1])
            pitch = noteNum + (octave - 1) * 12
            ticks = int(durationToBeats(note[1]) * resolution)
            if instruments[i] != -1:
                track.append(midi.NoteOnEvent(tick=0, channel=i,
                                              data=[pitch, volume[i]]))
                track.append(midi.NoteOffEvent(tick=ticks, channel=i,
                                               data=[pitch, 0]))
            else:
                track.append(midi.NoteOnEvent(tick=0, channel=9,
                                              data=[pitch, volume[i]]))
                track.append(midi.NoteOffEvent(tick=ticks, channel=9,
                                               data=[pitch, 0]))
        track.append(midi.EndOfTrackEvent(tick=0))
        pattern.append(track)
    midi.write_midifile('midi/' + name + '.mid', pattern)

def reachMusicGenerator(models, songName):
    song = []
    key = random.choice(KEY_SIGNATURES.keys())
    progNum = random.choice(list(range(len(PROG_ORDERS))))
    beatsPerChord = random.choice([2, 3, 4, 6])
    chordsPerProg = len(PROG_ORDERS[progNum])
    repeats = 3
    bpm = random.randint(60, 120)
    percussionInstruments = [PERCUSSION['bass'], PERCUSSION['bass'],
                             PERCUSSION['snare'], PERCUSSION['snare'],
                             PERCUSSION['hi hat']]
    instruments = [24, 24, 24, 36, 0, -1]
    volume = [70, 70, 70, 60, 70, 80]

    addChordsToSong(song, key, progNum, beatsPerChord, 5)
    addBassToSong(song, key, progNum, beatsPerChord, 4, NOTE_DURATIONS[3:6])
    for i in range(len(song)):
        repeatPhrase(song[i], repeats - 1)

    addMelodyToSong(models, song, key, progNum, beatsPerChord, repeats, 6)
    addPercussionToSong(song, percussionInstruments, beatsPerChord,
                        repeats * chordsPerProg)

    print 'Making song...'
    makeSongMidi(song, instruments, volume, songName, bpm)
    print 'Created song "' + songName + '"'
    return song

def reachMusicGeneratorOptions(models, songName, key, progNum, bpm):
    song = []
    beatsPerChord = random.choice([2, 3, 4, 6])
    chordsPerProg = len(PROG_ORDERS[progNum])
    repeats = 3
    percussionInstruments = [PERCUSSION['bass'], PERCUSSION['bass'],
                             PERCUSSION['snare'], PERCUSSION['snare'],
                             PERCUSSION['hi hat']]
    instruments = [24, 24, 24, 36, 0, -1]
    volume = [70, 70, 70, 60, 70, 80]

    addChordsToSong(song, key, progNum, beatsPerChord, 5)
    addBassToSong(song, key, progNum, beatsPerChord, 4, NOTE_DURATIONS[3:6])
    for i in range(len(song)):
        repeatPhrase(song[i], repeats - 1)

    addMelodyToSong(models, song, key, progNum, beatsPerChord, repeats, 6)
    addPercussionToSong(song, percussionInstruments, beatsPerChord,
                        repeats * chordsPerProg)

    print 'Making song...'
    makeSongMidi(song, instruments, volume, songName, bpm)
    print 'Created song "' + songName + '"'
    return song

def playSong(songName):
    '''
    uses pygame to play the generated song
    '''
    # pygame is only imported when needed because of incompatibility with the
    #  python version that comes with Apple devices
    import pygame
    pygame.mixer.init()
    pygame.mixer.music.load('midi/' + songName + '.mid')
    pygame.mixer.music.play()
    while pygame.mixer.music.get_busy() == True:
        continue

################################################################################

PROMPTS = [
"""
(1) Generate song lyrics by The Beatles
(2) Generate a song using data from Nintendo Gamecube
(3) Quit the music generator
>
""",
'''
Choose an option:
1) Autogenerate song
2) Create your own song
>
''',
'''
Choose a key:
Options: c, c#, d, eb, e, f, f#, g, ab, a, bb, b
>
''',
'''
Major or minor key?
Enter major/minor:
>
''',
'''
Choose a chord progression:
1) I, IV, V
2) I, V, VI, IV
3) I, IV, I, V, I
4) I, IV, V, I
>
''',
'''
Choose a tempo:
Options: fast, medium, slow
>
''',
'''
Would you like to listen to your song? (y/n)
>
'''
]

def getUserInput(prompt, validInputs):
    '''
    prints the prompt. continues to get the user's input until it's in
    validInputs
    '''
    input = raw_input(prompt)
    while not input in validInputs:
        print 'Invalid input.'
        input = raw_input(prompt)
    return input

def main():
    """
    Requires: Nothing
    Modifies: Nothing
    Effects:  This is your main function, which is done for you. It runs the
              entire generator program for both the reach and the core.

              It prompts the user to choose to generate either lyrics or music.
    """
    print('Starting program and loading data...')
    lyricsModels = trainLyricModels(LYRICSDIRS)
    musicModels = trainMusicModels(MUSICDIRS)
    print('Data successfully loaded')

    print('Welcome to the ' + TEAM + ' music generator!')
    while True:
        try:
            userInput = int(raw_input(PROMPTS[0]))
            if userInput == 1:
                runLyricsGenerator(lyricsModels)
            elif userInput == 2:

                choice = int(getUserInput(PROMPTS[1], ['1', '2']))
                if choice == 1:
                    songName = raw_input('What would you like to name your song? ')
                    song = reachMusicGenerator(musicModels, songName)
                    #createChord(song)
                    choice = getUserInput(PROMPTS[6], ['y', 'n'])
                    if choice == 'y':
                        playSong(songName)
                else:
                    key = getUserInput(PROMPTS[2],
                                          ['c', 'c#', 'd', 'eb', 'e', 'f', 'f#',
                                           'g', 'ab', 'a', 'bb', 'b'])
                    key += ' ' + getUserInput(PROMPTS[3], ['major', 'minor'])
                    progNum = int(getUserInput(PROMPTS[4],
                                               ['1', '2', '3', '4'])) - 1
                    bpm = getUserInput(PROMPTS[5], ['fast', 'medium', 'slow'])
                    if bpm == 'fast':
                        bpm = 120
                    elif bpm == 'medium':
                        bpm = 90
                    else:
                        bpm = 60
                    songName = raw_input('What would you like to name your song? ')
                    song = reachMusicGeneratorOptions(musicModels, songName, key,
                                               progNum, bpm)
                    #createChord(song)
                    choice = getUserInput(PROMPTS[6], ['y', 'n'])
                    if choice == 'y':
                        playSong(songName)

            elif userInput == 3:
                print('Thank you for using the ' + TEAM + ' music generator!')
                sys.exit()
            else:
                print("Invalid option!")
        except ValueError:
            print("Please enter a number")

def functionTests():

    # testing createMajorChord and createMinorChord
    # for note in chromNotesLetter:
    #     print chromNotesLetter[note], createMajorChord(note), \
    #         createMinorChord(note)

    # testing chordProg
    # progs = chordProg('c major')
    # progNum = 3
    # for root in PROG_ORDERS[progNum]:
    #     print progs[progNum][root]

    # testing durationToBeats and beatsToDuration
    # for duration in NOTE_DURATIONS:
    #     print durationToBeats(duration),\
    #         beatsToDuration(durationToBeats(duration))

    # testing limitPhraseLength and repeatPhrase
    # testPhrase = [('c4', 4), ('d4', 2), ('e4', -2), ('f4', 1)]
    # limitPhraseLength(testPhrase, 4)
    # print testPhrase
    # repeatPhrase(testPhrase, 3)
    # print testPhrase

    # testing makeBoosted
    # testPhrase = [('c4', 4), ('d4', 2), ('e4', -2), ('f4', 1)]
    # makeBoosted(testPhrase)
    # print testPhrase

    # testing addChordsToSong and makeSong
    # song = []
    # addChordsToSong(song, 'c major', 0, 4, 4)
    # for i in range(len(song)):
    #     repeatPhrase(song[i], 4)
    #     makeBoosted(song[i])
    # for track in song:
    #     print track
    # instruments = [pysynth, pysynth, pysynth]
    # makeSong(song, instruments, [1, 0.3, 0.1], 'chords_volume', 120)

    # testing addBassToSong, addChordsToSong and makeSong
    # song = []
    # key = 'c major'
    # progNum = 2
    # beatsPerChord = 4
    # addChordsToSong(song, key, progNum, beatsPerChord, 4)
    # addBassToSong(song, key, progNum, beatsPerChord, 3, NOTE_DURATIONS[3:])
    # for i in range(len(song)):
    #     makeBoosted(song[i])
    #     repeatPhrase(song[i], 3)
    #     print song[i]
    # instruments = [pysynth, pysynth, pysynth, pysynth]
    # volume = [1, 0.3, 0.1, 0.1]
    # makeSong(song, instruments, volume, 'bass', 120)

    # test makeSongMidi and addMelody and addPercussion
    # print 'Training models...'
    # musicModels = trainMusicModels(MUSICDIRS)
    # input = 'y'
    # while input == 'y':
    #     song = []
    #     key = 'd major'
    #     progNum = 2
    #     beatsPerChord = 4
    #     repeats = 4
    #     chordsPerProg = len(PROG_ORDERS[progNum])
    #
    #     addChordsToSong(song, key, progNum, beatsPerChord, 5)
    #     addBassToSong(song, key, progNum, beatsPerChord, 4, NOTE_DURATIONS[3:6])
    #     for i in range(len(song)):
    #         repeatPhrase(song[i], repeats - 1)
    #
    #     addMelodyToSong(musicModels, song, key, progNum, beatsPerChord,
    #                     repeats, 6)
    #     percussionInstruments = [PERCUSSION['bass'], PERCUSSION['bass'],
    #                              PERCUSSION['snare'], PERCUSSION['snare'],
    #                              PERCUSSION['hi hat']]
    #     addPercussionToSong(song, percussionInstruments, beatsPerChord,
    #                         repeats * chordsPerProg)
    #
    #     instruments = [24, 24, 24, 36, 0, -1]
    #     volume = [70, 70, 70, 60, 100, 100]
    #     print 'Making song...'
    #     makeSongMidi(song, instruments, volume, 'chordsBassMelodyDrums', 120)
    #     print 'Done'
    #     input = raw_input('Make another song? (y/n): ')

    # test reachMusicGenerators
    # print 'Training models...'
    # musicModels = trainMusicModels(MUSICDIRS)
    # reachMusicGenerator(musicModels, 'reach')
    pass


#####---DATA VISUALIZATION OF REACH---#########################################

"""

def doCircleRibbonGraph(labels, matrix):
    ideo_colors=['rgba(122, 17, 17, 0.75)',
                 'rgba(122, 101, 17, 0.75)',
                 'rgba(47, 73, 6, 0.75)',
                 'rgba(5, 66, 72, 0.75)',
                 'rgba(4, 25, 72, 0.75)',
                 'rgba(107, 159, 249, 0.75)',
                 'rgba(107, 209, 219, 0.75)',
                 'rgba(117, 209, 119, 0.75)',
                 'rgba(117, 109, 219, 0.75)',
                 'rgba(217, 109, 219, 0.75)',
                 'rgba(117, 209, 119, 0.75)',
                 'rgba(166, 217, 106, 0.75)',
                 'rgba(166, 217, 106, 0.75)',
                 'rgba(117, 209, 119, 0.75)',
                 'rgba(107, 159, 249, 0.75)']


    def check_data(data_matrix):
        L, M=data_matrix.shape
        if L!=M:
            raise ValueError('Data array must have (n,n) shape')
        return L

    L=check_data(matrix)



    PI=np.pi

    def moduloAB(x, a, b):
        
            if a>=b:
                raise ValueError('Incorrect interval ends')
            y=(x-a)%(b-a)
            return y+b if y<0 else y+a

    def test_2PI(x):
        return 0<= x <2*PI



    row_sum=[np.sum(matrix[k,:]) for k in range(L)]


    gap=2*PI*0.005
    ideogram_length=2*PI*np.asarray(row_sum)/sum(row_sum)-gap*np.ones(L)



    def get_ideogram_ends(ideogram_len, gap):
        ideo_ends=[]
        left=0
        for k in range(len(ideogram_len)):
            right=left+ideogram_len[k]
            ideo_ends.append([left, right])
            left=right+gap
        return ideo_ends

    ideo_ends=get_ideogram_ends(ideogram_length, gap)
    ideo_ends



    def make_ideogram_arc(R, phi, a=50):
        # R is the circle radius
        # phi is the list of ends angle coordinates of an arc
        # a is a parameter that controls the number of points to be evaluated on an arc
        if not test_2PI(phi[0]) or not test_2PI(phi[1]):
            phi=[moduloAB(t, 0, 2*PI) for t in phi]
        length=(phi[1]-phi[0])% 2*PI
        nr=5 if length<=PI/4 else int(a*length/PI)

        if phi[0] < phi[1]:
            theta=np.linspace(phi[0], phi[1], nr)
        else:
            phi=[moduloAB(t, -PI, PI) for t in phi]
            theta=np.linspace(phi[0], phi[1], nr)
        return R*np.exp(1j*theta)



    z=make_ideogram_arc(1.3, [11*PI/6, PI/17])
    




    def map_data(data_matrix, row_value, ideogram_length):
        mapped=np.zeros(data_matrix.shape)
        for j  in range(L):
            mapped[:, j]=ideogram_length*data_matrix[:,j]/row_value
        return mapped

    mapped_data=map_data(matrix, row_sum, ideogram_length)
    mapped_data



    idx_sort=np.argsort(mapped_data, axis=1)
    idx_sort



    def make_ribbon_ends(mapped_data, ideo_ends,  idx_sort):
        L=mapped_data.shape[0]
        ribbon_boundary=np.zeros((L,L+1))
        for k in range(L):
            start=ideo_ends[k][0]
            ribbon_boundary[k][0]=start
            for j in range(1,L+1):
                J=idx_sort[k][j-1]
                ribbon_boundary[k][j]=start+mapped_data[k][J]
                start=ribbon_boundary[k][j]
        return [[(ribbon_boundary[k][j],ribbon_boundary[k][j+1] ) for j in range(L)] for k in range(L)]

    ribbon_ends=make_ribbon_ends(mapped_data, ideo_ends,  idx_sort)
    


    def control_pts(angle, radius):
        
        if len(angle)!=3:
            raise InvalidInputError('angle must have len =3')
        b_cplx=np.array([np.exp(1j*angle[k]) for k in range(3)])
        b_cplx[1]=radius*b_cplx[1]
        return zip(b_cplx.real, b_cplx.imag)



    def ctrl_rib_chords(l, r, radius):

        if len(l)!=2 or len(r)!=2:
            raise ValueError('the arc ends must be elements in a list of len 2')
        return [control_pts([l[j], (l[j]+r[j])/2, r[j]], radius) for j in range(2)]



    ribbon_color=[L*[ideo_colors[k]] for k in range(L)]



    def make_q_bezier(b):
        
        if len(b)!=3:
            raise valueError('control poligon must have 3 points')
        A, B, C=b
        return 'M '+str(A[0])+',' +str(A[1])+' '+'Q '+\
                    str(B[0])+', '+str(B[1])+ ' '+\
                    str(C[0])+', '+str(C[1])

    b=[(1,4), (-0.5, 2.35), (3.745, 1.47)]

    make_q_bezier(b)



    def make_ribbon_arc(theta0, theta1):

        if test_2PI(theta0) and test_2PI(theta1):
            if theta0 < theta1:
                theta0= moduloAB(theta0, -PI, PI)
                theta1= moduloAB(theta1, -PI, PI)
                if theta0*theta1>0:
                    raise ValueError('incorrect angle coordinates for ribbon')

            nr=int(40*(theta0-theta1)/PI)
            if nr<=2: nr=3
            theta=np.linspace(theta0, theta1, nr)
            pts=np.exp(1j*theta)

            string_arc=''
            for k in range(len(theta)):
                string_arc+='L '+str(pts.real[k])+', '+str(pts.imag[k])+' '
            return   string_arc
        else:
            raise ValueError('the angle coordinates for an arc side of a ribbon must be in [0, 2*pi]')

    make_ribbon_arc(np.pi/3, np.pi/6)



    def make_layout(title, plot_size):
        axis=dict(showline=False,
              zeroline=False,
              showgrid=False,
              showticklabels=False,
              title=''
              )

        return Layout(title=title,
                      xaxis=XAxis(axis),
                      yaxis=YAxis(axis),
                      showlegend=False,
                      width=plot_size,
                      height=plot_size,
                      margin=Margin(t=25, b=25, l=25, r=25),
                      hovermode='closest',
                      shapes=[]
                      
                     )



    def make_ideo_shape(path, line_color, fill_color):

        return  dict(
                      line=Line(
                      color=line_color,
                      width=0.45
                     ),

                path=  path,
                type='path',
                fillcolor=fill_color,
            )



    def make_ribbon(l, r, line_color, fill_color, radius=0.2):

        poligon=ctrl_rib_chords(l,r, radius)
        b,c =poligon

        return  dict(
                    line=Line(
                    color=line_color, width=0.5
                ),
                path=  make_q_bezier(b)+make_ribbon_arc(r[0], r[1])+
                       make_q_bezier(c[::-1])+make_ribbon_arc(l[1], l[0]),
                type='path',
                fillcolor=fill_color,
            )

    def make_self_rel(l, line_color, fill_color, radius):
   
        b=control_pts([l[0], (l[0]+l[1])/2, l[1]], radius)
        return  dict(
                    line=Line(
                    color=line_color, width=0.5
                ),
                path=  make_q_bezier(b)+make_ribbon_arc(l[1], l[0]),
                type='path',
                fillcolor=fill_color,
            )

    def invPerm(perm):
   
        inv = [0] * len(perm)
        for i, s in enumerate(perm):
            inv[s] = i
        return inv

    layout=make_layout('Chord diagram', 400)



    radii_sribb=[0.4, 0.30, 0.35, 0.39, 0.12,0.4, 0.30, 0.35, 0.39, 0.12,0.4, 0.30, 0.35]



    ribbon_info=[]
    for k in range(L):

        sigma=idx_sort[k]
        sigma_inv=invPerm(sigma)
        for j in range(k, L):
            if matrix[k][j]==0 and matrix[j][k]==0: continue
            eta=idx_sort[j]
            eta_inv=invPerm(eta)
            l=ribbon_ends[k][sigma_inv[j]]

            if j==k:
                layout['shapes'].append(make_self_rel(l, 'rgb(175,175,175)' ,
                                        ideo_colors[k], radius=radii_sribb[k]))
                z=0.9*np.exp(1j*(l[0]+l[1])/2)
               
                if j == 0 :
                    text=labels[k]+' played '+ '{:d}'.format(matrix[k][k])+' notes ',
                    ribbon_info.append(Scatter(x=z.real,
                                            y=z.imag,
                                            mode='markers',
                                            marker=Marker(size=0.5, color=ideo_colors[k]),
                                            text=text,
                                            hoverinfo='text'
                                            )
                                   )
            else:
                r=ribbon_ends[j][eta_inv[k]]
                zi=0.9*np.exp(1j*(l[0]+l[1])/2)
                zf=0.9*np.exp(1j*(r[0]+r[1])/2)

                texti=labels[k]+' played ' + labels[j]+ ' ' +'{:d}'.format(matrix[k][j])+' times '+\
                      '',
                textf=labels[k]+' played ' + labels[j]+ ' ' +'{:d}'.format(matrix[k][j])+' times '+\
                      '',

                ribbon_info.append(Scatter(x=zi.real,
                                           y=zi.imag,
                                           mode='markers',
                                           marker=Marker(size=0.5, color=ribbon_color[k][j]),
                                           text=texti,
                                           hoverinfo='text'
                                           )
                                  ),
                ribbon_info.append(Scatter(x=zf.real,
                                           y=zf.imag,
                                           mode='markers',
                                           marker=Marker(size=0.5, color=ribbon_color[k][j]),
                                           text=textf,
                                           hoverinfo='text'
                                           )
                                  )
                r=(r[1], r[0])
                
             
                layout['shapes'].append(make_ribbon(l, r, 'rgb(175,175,175)' , ribbon_color[k][j]))



    ideograms=[]
    for k in range(len(ideo_ends)):
        z= make_ideogram_arc(1.1, ideo_ends[k])
        zi=make_ideogram_arc(1.0, ideo_ends[k])
        m=len(z)
        n=len(zi)
        if k == 0 :
            ideograms.append(Scatter(x=z.real,
                                    y=z.imag,
                                    mode='lines',
                                    line=Line(color=ideo_colors[k], shape='spline', width=0.25),
                                    text=labels[k]+' played '+'{:d}'.format(row_sum[k]) + ' notes ',
                                    hoverinfo='text'
                                    )
                                    )

        else :
            ideograms.append(Scatter(x=z.real,
                                    y=z.imag,
                                    mode='lines',
                                    line=Line(color=ideo_colors[k], shape='spline', width=0.25),
                                    text=labels[k],
                                    hoverinfo='text'
                                    )
                                    )




        path='M '
        for s in range(m):
            path+=str(z.real[s])+', '+str(z.imag[s])+' L '

        Zi=np.array(zi.tolist()[::-1])

        for s in range(m):
            path+=str(Zi.real[s])+', '+str(Zi.imag[s])+' L '
        path+=str(z.real[0])+' ,'+str(z.imag[0])

        layout['shapes'].append(make_ideo_shape(path,'rgb(150,150,150)' , ideo_colors[k]))



    data = Data(ideograms+ribbon_info)
    fig = Figure(data=data, layout=layout)

    plot_url = py.plot(fig, filename='Chord Diagram')



def getFrequencies(song) :

    name = 'Reach Generated Music'
    c = 'c'
    cSharp = 'c#'
    d = 'd'
    eFlat = 'eb'
    e = 'e'
    f = 'f'
    fSharp = 'f#'
    g = 'g'
    aFlat = 'ab'
    a = 'a'
    bFlat = 'bb'
    b = 'b'



    categories = [name,c,cSharp,d,eFlat,e,f,fSharp,g,aFlat,a,bFlat,b]
    data = [0,0,0,0,0,0,0,0,0,0,0,0,0]





    for chan in song :
        for tup in chan :
            currentNote = tup[0][0:-1]
            
            data[categories.index(currentNote)] += 1

    return [categories, data]

def createChord(song) :

    data = getFrequencies(song)


    labels= data[0]
    matrix=np.array([data[1],
    [0,50,0,0,0,0,0,0,0,0,0,0,0],
    [0,0,50,0,0,0,0,0,0,0,0,0,0],
    [0,0,0,50,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,50,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,50,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,50,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,50,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,50,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,50,0,0,0],
    [0,0,0,0,0,0,0,0,0,0,50,0,0],
    [0,0,0,0,0,0,0,0,0,0,0,50,0],
    [0,0,0,0,0,0,0,0,0,0,0,0,50]]
    , dtype=int)
    
    doCircleRibbonGraph(labels, matrix)
"""


if __name__ == '__main__':
    main()
    pass

