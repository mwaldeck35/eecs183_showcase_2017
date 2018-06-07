'''
Larry Zhao
Last Edited: 11/27
'''

import random
from nGramModel import *

class TrigramModel(NGramModel):

    def __init__(self):
        """
        Requires: nothing
        Modifies: self (this instance of the NGramModel object)
        Effects:  this is the TrigramModel constructor, which is done
                  for you. It allows TrigramModel to access the data
                  from the NGramModel class.
        """
        super(TrigramModel, self).__init__()

    def trainModel(self, text):
        """
        Requires: text is a list of lists of strings
        Modifies: self.nGramCounts, a three-dimensional dictionary. For
                  examples and pictures of the TrigramModel's version of
                  self.nGramCounts, see the spec.
        Effects:  this function populates the self.nGramCounts dictionary,
                  which has strings as keys and dictionaries as values,
                  where those inner dictionaries have strings as keys
                  and dictionaries of {string: integer} pairs as values.

                  Note: make sure to use the return value of prepData to
                  populate the dictionary, which will allow the special
                  symbols to be included as their own tokens in
                  self.nGramCounts. For more details, see the spec.
        """
        '''
        Algorithm:
        call prepData on the lyrics
        loop through all the sentences in lyrics
        loop through all the words except the last two in each sentence
        get 3 words at a time
        check if the first word is in the dictionary
            if so:
                repeat with the next word
            if not:
                make a new pair; key = first word, value = 2d dictionary of 
                next words
        '''
        lyrics = self.prepData(text)
        nGramCounts = {}
        for sentence in lyrics:
            for i in range(len(sentence) - 2):
                firstWord = sentence[i]
                secondWord = sentence[i + 1]
                thirdWord = sentence[i + 2]
                if firstWord in nGramCounts:
                    if secondWord in nGramCounts[firstWord]:
                        if thirdWord in nGramCounts[firstWord][secondWord]:
                            nGramCounts[firstWord][secondWord][thirdWord] += 1
                        else:
                            nGramCounts[firstWord][secondWord][thirdWord] = 1
                    else:
                        nGramCounts[firstWord][secondWord] = {thirdWord: 1}
                else:
                    nGramCounts[firstWord] = {secondWord: {thirdWord: 1}}
        self.nGramCounts = nGramCounts

    def trainingDataHasNGram(self, sentence):
        """
        Requires: sentence is a list of strings, and len(sentence) >= 2
        Modifies: nothing
        Effects:  returns True if this n-gram model can be used to choose
                  the next token for the sentence. For explanations of how this
                  is determined for the TrigramModel, see the spec.
        """
        '''
        Algorithm:
        get the last two words in the sentence
        check if the first is a key in the first level of nGramCounts
            if so: check if the second is a key in the second level
            if not: return false
        '''
        firstWord = sentence[-2]
        secondWord = sentence[-1]
        if firstWord in self.nGramCounts:
            return secondWord in self.nGramCounts[firstWord]
        else:
            return False

    def getCandidateDictionary(self, sentence):
        """
        Requires: sentence is a list of strings, and trainingDataHasNGram
                  has returned True for this particular language model
        Modifies: nothing
        Effects:  returns the dictionary of candidate next words to be added
                  to the current sentence. For details on which words the
                  TrigramModel sees as candidates, see the spec.
        """
        '''
        Algorithm:
        return the innermost dictionary from the last two words
        '''
        firstWord = sentence[-2]
        secondWord = sentence[-1]
        return self.nGramCounts[firstWord][secondWord]


###############################################################################
# Main
###############################################################################

if __name__ == '__main__':
    # Add your tests here
    text = [ ['the', 'quick', 'brown', 'fox'],
             ['the', 'quick', 'lazy', 'dog'],
             ['the', 'quick', 'brown', 'fox'],
             ['the', 'quick', 'brown', 'cat'] ]
    trigramModel = TrigramModel()
    trigramModel.trainModel(text)
    print trigramModel.nGramCounts

    sentence = [ 'the', 'quick', 'brown' ]
    # true
    print trigramModel.trainingDataHasNGram(sentence)
    # fox: 2, cat: 1
    print trigramModel.getCandidateDictionary(sentence)

    sentence = [ '^:::^', 'the', 'quick' ]
    # true
    print trigramModel.trainingDataHasNGram(sentence)
    # brown: 3, lazy: 1
    print trigramModel.getCandidateDictionary(sentence)

    sentence = [ 'the', 'fast', 'brown' ]
    # false
    print trigramModel.trainingDataHasNGram(sentence)