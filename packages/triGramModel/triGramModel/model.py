import numpy as np
import random
import string
import re
import joblib
import textwrap

from triGramModel.config import config
from triGramModel.processing import data_management as dm

class cipherDecrypter():
    def __init__(self, nchars = 26):
        self.uni = np.zeros(nchars)
        self.bi = np.ones((nchars,nchars))
        self.tri = np.ones((nchars,nchars,nchars))

    def _update_tri_transition(self, ch1, ch2, ch3):
        # ord('a') = 97, ord('b') = 98, ...
        i = ord(ch1) - 97
        j = ord(ch2) - 97
        k = ord(ch3) - 97
        self.tri[i,j,k] += 1

    def _update_bi_transition(self, ch1, ch2):
        # ord('a') = 97, ord('b') = 98, ...
        i = ord(ch1) - 97
        j = ord(ch2) - 97
        self.bi[i,j] += 1

    def _update_uni(self, ch):
        # ord('a') = 97, ord('b') = 98, ...
        i = ord(ch) - 97
        self.uni[i] += 1


    def _get_word_prob(self, word):
        # probability of string 'ABC' in that order is:
        # pr(ABC) = pr(C|AB)pr(B|A)pr(A)
        # log(pr(ABC)) = log(pr(C|AB)) + log(pr(B|A)) + log(pr(A))
        i = ord(word[0]) - 97
        logp = np.log(self.uni[i])

        if len(word) > 1:
            ch = word[1]
            j = ord(ch) - 97
            logp += np.log(self.bi[i,j])

            for ch in word[2:]:
                k = ord(ch) - 97
                logp += np.log(self.tri[i,j,k])
                i = j
                j = k

        return logp

    def _get_sequence_prob(self, words):
        # if input is a string, then split into an array of tokens
        if type(words) == str:
            words = words.split()

        logp = 0
        for word in words:
            logp += self._get_word_prob(word)

        return logp

    def fit(self, train_file):

        regex = re.compile('[^a-zA-z]')

        #load in words
        for line in open(train_file, encoding = 'utf8'):
            line = line.rstrip()

            # there are blank lines in the file
            if line:
                # replace all non-alpha characters with space
                line = regex.sub(' ', line) 

                # split the tokens in the line and lowercase
                tokens = line.lower().split()

                for token in tokens:
                    ## update the model
                    # first letter
                    ch0 = token[0]
                    self._update_uni(ch0)

                    if len(token) > 1:
                        # second letter
                        ch1 = token[1]
                        self._update_bi_transition( ch0, ch1)

                        # other letters
                        for ch2 in token[2:]:
                            self._update_tri_transition( ch0, ch1, ch2)
                            ch0 = ch1
                            ch1 = ch2

        # normalize the probabilities
        self.uni/= self.uni.sum()
        self.bi/= self.bi.sum(axis=1, keepdims=True)
        self.tri/= self.tri.sum(axis=(1,2), keepdims = True)

    def _evolve_offspring(self, dna_pool, n_children):
        # make n_children per offspring
        offspring = []

        for dna in dna_pool:
            for _ in range(n_children):
                copy = dna.copy()
                j = np.random.randint(len(copy))
                k = np.random.randint(len(copy))

                # switch
                tmp = copy[j]
                copy[j] = copy[k]
                copy[k] = tmp
                offspring.append(copy)

        return offspring + dna_pool

    def predict(self, test):

        ### run an evolutionary algorithm to decode the message

        # this is our initialization point
        dna_pool = []
        for _ in range(20):
            dna = list(string.ascii_lowercase)
            random.shuffle(dna)
            dna_pool.append(dna)
        
        num_iters = config.ITERS
        scores = np.zeros(num_iters)
        best_dna = None
        best_map = None
        best_score = float('-inf')
        encoded_message = test
        letters = list(string.ascii_lowercase)
            
        for i in range(num_iters):
            if i > 0:
                # get offspring from the current dna pool
                dna_pool = self._evolve_offspring( dna_pool, 6)

            # calculate score for each dna
            dna2score = {}
            for dna in dna_pool:
                # populate the map
                current_map = {}
                for k, v in zip(letters, dna):
                    current_map[k] = v 

                decoded_message = dm.decode_message(encoded_message, current_map)
                score = self._get_sequence_prob( decoded_message)

                # store it
                # needs to be a string to be a dict key
                dna2score[''.join(dna)] = score

                # record the best so far
                if score > best_score:
                    best_dna = dna
                    best_map = current_map
                    best_score = score

            # average score for this generation
            scores[i] = np.mean(list(dna2score.values()))

            # keep the best 5 dna
            # also turn them back into list of single chars
            sorted_dna = sorted(dna2score.items(), key=lambda x: x[1], reverse=True)
            dna_pool = [list(k) for k, v in sorted_dna[:5]]

            if (i+1) % 200 == 0:
                print("iter:", i+1, "score:", scores[i], "best so far:", best_score)

        # save best map
        save_path = config.TRAINED_MODEL_DIR / config.BEST_MAP_FILE_NAME
        joblib.dump(best_map,  save_path)


    def score(self, encoded_message, original_message, best_map, true_map):

        decoded_message = dm.decode_message(encoded_message, best_map)
        regex = re.compile('[^a-zA-z]')

        print("LL of decoded message:", self._get_sequence_prob(decoded_message))
        print("LL of true message:", self._get_sequence_prob(regex.sub(' ', original_message.lower())))

        # which letters are wrong?
        for true, v in true_map.items():
            pred = best_map[v]
            if true != pred:
                print("true: %s, pred %s" %(true, pred))

        # print the final decoded message
        print("Decoded message:\n", textwrap.fill(decoded_message))

        print("\nTrue message:\n", original_message)
