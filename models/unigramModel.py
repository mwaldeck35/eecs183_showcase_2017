import random
from nGramModel import *

class UnigramModel(NGramModel):

    def __init__(self):
        """
        Requires: nothing
        Modifies: self (this instance of the UnigramModel object)
        Effects:  this is the UnigramModel constructor, which is done
                  for you. It allows UnigramModel to access the data
                  in the NGramModel class by calling the NGramModel
                  constructor.
        """
        super(UnigramModel, self).__init__()

    def trainModel(self, text):
        """
        Requires: text is a list of lists of strings
        Modifies: self.nGramCounts
        Effects:  this function populates the self.nGramCounts dictionary,
                  which is a dictionary of {string: integer} pairs.
                  For further explanation of UnigramModel's version of
                  self.nGramCounts, see the spec.

                  Note: make sure to use the return value of prepData to
                  populate the dictionary, which will allow the special
                  symbols to be included as their own tokens in
                  self.nGramCounts. For more details, see the spec.
        """

        lyrics = self.prepData(text)
        nGramCounts = {}
        for sentence in lyrics:
            for word in sentence:
                if word != '^::^' and word != '^:::^':
                    if word in nGramCounts:
                        nGramCounts[word] += 1
                    else:
                        nGramCounts[word] = 1

        self.nGramCounts = nGramCounts




    def trainingDataHasNGram(self, sentence):
        """
        Requires: sentence is a list of strings
        Modifies: nothing
        Effects:  returns True if this n-gram model can be used to choose
                  the next token for the sentence. For explanations of how this
                  is determined for the UnigramModel, see the spec.
        """
        return len(self.nGramCounts) != 0


    def getCandidateDictionary(self, sentence):
        """
        Requires: sentence is a list of strings, and trainingDataHasNgGram
                  has returned True for this particular language model
        Modifies: nothing
        Effects:  returns the dictionary of candidate next words to be added
                  to the current sentence. For details on which words the
                  UnigramModel sees as candidates, see the spec.
        """
        return self.nGramCounts

###############################################################################
# Main
###############################################################################

if __name__ == '__main__':
    # Add your test cases here
    text = [ ['the', 'quick', 'brown', 'fox'], ['the', 'lazy', 'dog'], ['the', 'quick', 'brown', 'cat'] ]

    unigramModel = UnigramModel()
    unigramModel.trainModel(text)
    print unigramModel.nGramCounts
    print unigramModel.getCandidateDictionary(text)
    #true
    print unigramModel.trainingDataHasNGram(text)

    sentence1 = []
    unigramModel1 = UnigramModel()
    unigramModel1.trainModel(sentence1)
    print unigramModel1.nGramCounts
    print unigramModel1.getCandidateDictionary(sentence1)
    #false
    print unigramModel1.trainingDataHasNGram(sentence1)
