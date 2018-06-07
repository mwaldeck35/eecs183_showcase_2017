import random
import sys
import json
from musicInfo import *

class NGramModel(object):

    def __init__(self):
        """
        Requires: nothing
        Modifies: self (this instance of the NGramModel object)
        Effects:  This is the NGramModel constructor. It sets up an empty
                  dictionary as a member variable. It is called from the
                  constructors of the NGramModel child classes. This
                  function is done for you.
        """
        self.nGramCounts = {}

    def __str__(self):
        """
        Requires: nothing
        Modifies: nothing
        Effects:  Returns the string to print when you call print on an
                  NGramModel object. This string will be formatted in JSON
                  and display the currently trained dataset.
                  This function is done for you.
        """
        return self.__class__.__name__ + ':\n' +\
            json.dumps(
                       self.nGramCounts,
                       sort_keys=True,
                       indent=4,
                       separators=(',', ': ')
            )

    def prepData(self, text):
        """
        Requires: text is a list of lists of strings
        Modifies: nothing
        Effects:  returns a copy of text where each inner list starts with
                  the symbols '^::^' and '^:::^', and ends with the symbol
                  '$:::$'. For example, if an inner list in text were
                  ['hello', 'goodbye'], that list would become
                  ['^::^', '^:::^', 'hello', 'goodbye', '$:::$'] in the
                  returned copy.
        """
        textCopy = []
        for line in text:
            textCopy.append(['^::^', '^:::^'] + line + ['$:::$'])
        return textCopy

    def trainModel(self, text):
        """
        Requires: text is a list of lists of strings
        Modifies: self.nGramCounts
        Effects:  this function populates the self.nGramCounts dictionary.
                  It does not need to be modified here because you will
                  override it in the NGramModel child classes according
                  to the spec.
        """
        pass

    def trainingDataHasNGram(self, sentence):
        """
        Requires: sentence is a list of strings, and trainingDataHasNGram
                  has returned True for this particular language model
        Modifies: nothing
        Effects:  returns a bool indicating whether or not this n-gram model
                  can be used to choose the next token for the current
                  sentence. This function does not need to be modified because
                  you will override it in NGramModel child classes according
                  to the spec.
        """
        pass

    def getCandidateDictionary(self, sentence):
        """
        Requires: sentence is a list of strings
        Modifies: nothing
        Effects:  returns the dictionary of candidate next words to be added
                  to the current sentence. This function does not need to be
                  modified because you will override it in the NGramModel child
                  classes according to the spec.
        """
        pass

    def weightedChoice(self, candidates):
        """
        Requires: candidates is a dictionary; the keys of candidates are items
                  you want to choose from and the values are integers
        Modifies: nothing
        Effects:  returns a candidate item (a key in the candidates dictionary)
                  based on the algorithm described in the spec.
        """
        '''
        Algorithm:
        outlined in the spec
        '''
        tokens = candidates.keys()
        counts = candidates.values()
        totalCount = 0
        cumulative = []
        for count in counts:
            # the previous item plus the current one
            totalCount += count
            cumulative.append(totalCount)
        randNum = random.randrange(0, cumulative[-1])
        for i in range(len(cumulative)):
            if cumulative[i] > randNum:
                return tokens[i]


    def getNextToken(self, sentence):
        """
        Requires: sentence is a list of strings, and this model can be used to
                  choose the next token for the current sentence
        Modifies: nothing
        Effects:  returns the next token to be added to sentence by calling
                  the getCandidateDictionary and weightedChoice functions.
                  For more information on how to put all these functions
                  together, see the spec.
        """

        return self.weightedChoice(self.getCandidateDictionary(sentence))

    def getNextNote(self, musicalSentence, possiblePitches):
        """
        Requires: musicalSentence is a list of PySynth tuples,
                  possiblePitches is a list of possible pitches for this
                  line of music (in other words, a key signature), and this
                  model can be used to choose the next note for the current
                  musical sentence
        Modifies: nothing
        Effects:  returns the next note to be added to the "musical sentence".
                  For details on how to do this and how this will differ
                  from getNextToken, see the spec.
        """
        allCandidates = self.getCandidateDictionary(musicalSentence)
        realCandidates = {}
        for x in allCandidates:
            if x[0][:-1] in possiblePitches or x == '$::$':
                realCandidates[x] = allCandidates[x]
        if len(realCandidates) != 0:
            return self.weightedChoice(realCandidates)
        else:
            randomPitch = random.choice(possiblePitches) + '4'
            randomLength = random.choice(NOTE_DURATIONS)
            return (randomPitch, randomLength)

###############################################################################
# Main
###############################################################################

if __name__ == '__main__':
    # Add your tests here
    text = [ ['the', 'quick', 'brown', 'fox'], ['the', 'lazy', 'dog'] ]
    choices = { 'the': 2, 'quick': 1, 'brown': 1 }
    nGramModel = NGramModel()

    # weightedChoice tests
    testCandidates = {'green': 10, 'eggs': 2, 'and': 3, 'ham': 3}
    numGreen, numEggs, numAnd, numHam = (0, 0, 0, 0)
    numTrials = 1000.0
    for i in range(int(numTrials)):
        choice = nGramModel.weightedChoice(testCandidates)
        if choice == 'green':
            numGreen += 1
        elif choice == 'eggs':
            numEggs += 1
        elif choice == 'and':
            numAnd += 1
        elif choice == 'ham':
            numHam += 1
    print 'Green: expected:', 10 / 18.0, 'actual:', numGreen / numTrials
    print 'Eggs: expected:', 2 / 18.0, 'actual:', numEggs / numTrials
    print 'And: expected:', 3 / 18.0, 'actual:', numAnd / numTrials
    print 'Ham: expected:', 3 / 18.0, 'actual:', numHam / numTrials
