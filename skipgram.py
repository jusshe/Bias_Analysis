# My implementation (with lots of help from plenty of tutorials & explanatory guides) of 
# word2vec (skip-gram) using numpy. It is flawed; namely, I realized I calculate loss at 
# the final layer (after softmax), where the correct output that I compare the output layer against
# is a matrix with 1 at each row for a context word and 0 at each row for a word that doesn't appear 
# in context of the center word being considered. This means the model is not taking into account 
# how frequently words appear in the same context -- only if they do. I use a local file containing
# the novel The Great Gatsby in the example below.

# Sources:

# https://www.nltk.org/index.html
# http://sites.science.oregonstate.edu/math/home/programs/undergrad/CalculusQuestStudyGuides/vcalc/grad/grad.html
# https://towardsdatascience.com/introduction-to-word-embedding-and-word2vec-652d0c2060fa
# https://towardsdatascience.com/understanding-backpropagation-algorithm-7bb3aa2f95fd
# https://medium.com/@songxia.sophia/word-embedding-of-brown-corpus-using-python-ec09ff4cbf4f
# https://www.geeksforgeeks.org/implement-your-own-word2vecskip-gram-model-in-python/

import numpy as np
import string
from nltk.corpus import stopwords


class word2vec():
    def __init__(self):
        self.corpus = corpus
        self.corpus_len = len(corpus)
        self.vocab = 0
        self.types_dict = {}
        self.word_dim = settings['word_dim']
        self.rate = settings['learning_rate']
        self.epochs = settings['epochs']
        self.window = settings['window_size']
        self.training_data = {}
        self.word_to_row = {}
        self.in_layer = []
        self.weight1 = []
        self.hidden_layer = []
        self.weight2 = []
        self.out_layer = []
        self.soft_out = []
        self.loss = 0

    def prep_for_training(self):
        # create dict of distinct words with array values and count types
        index = 0
        for word in self.corpus:
            self.training_data[word] = []
            if word not in self.word_to_row:
                self.word_to_row[word] = index
                index += 1
            if word not in self.types_dict:
                self.types_dict[word] = 0
            else:
                self.types_dict[word] += 1

        # fill dict arrays with words that appear in context of corpus[i]
        for i in range(self.corpus_len):
            for j in range(i - self.window, i + self.window + 1):
                if 0 <= j < self.corpus_len and self.corpus[j] != self.corpus[i]:
                    if self.corpus[j] not in self.training_data[self.corpus[i]]:
                        self.training_data[self.corpus[i]].append(self.corpus[j])

        self.vocab = len(self.training_data)

        self.weight1 = np.random.uniform(-0.8, 0.8, (self.vocab, self.word_dim))
        self.weight2 = np.random.uniform(-0.8, 0.8, (self.word_dim, self.vocab))

    def initial_analysis(self):
        avg_freq = 0
        print("Types: " + str(self.vocab))
        for _type in self.types_dict.keys():
            avg_freq += self.types_dict[_type]
        avg_freq = avg_freq/self.vocab
        print("Average freq of types: " + str(avg_freq))


    def train(self):
        for i in range(self.epochs):
            self.loss = 0
            for word in self.training_data.keys():
                # set up in_layer
                self.in_layer = [[0] for i in range(self.vocab)]
                self.in_layer[self.word_to_row[word]] = [1]

                # forward propagation
                self.hidden_layer = [[i] for i in self.weight1[self.word_to_row[word]]]
                self.out_layer = np.transpose(np.dot(np.transpose(self.hidden_layer), self.weight2))
                e_x = np.exp(self.out_layer - np.max(self.out_layer))
                self.soft_out = e_x / e_x.sum()

                # backpropagation
                correct_out = [[0] for i in range(self.vocab)]
                for out_word in self.training_data[word]:
                    correct_out[self.word_to_row[out_word]] = [1]
                e = self.soft_out - correct_out
                dldw2 = np.dot(self.hidden_layer, np.transpose(e))
                dldw1 = np.dot(self.in_layer, np.transpose(np.dot(self.weight2, e)))
                self.weight2 = self.weight2 - self.rate * dldw2
                self.weight1 = self.weight1 - self.rate * dldw1

                # calculate loss
                context_words = 0
                for context_word in self.training_data[word]:
                    self.loss += -1 * self.out_layer[self.word_to_row[context_word]][0]
                    context_words += 1
                self.loss += context_words * np.log(np.sum(np.exp(self.out_layer)))

            print("epoch: ", i, ", loss = ", self.loss)

# Accepts corpus as single string
def preprocessing(text):
    processed = []
    sentences = text.split(".")   # NOTE: will create empty sentences in the case of consecutive periods
    for i in range(len(sentences)):
        # remove leading and trailing whitespace
        sentences[i] = sentences[i].strip()
        # break into array of words; remove punctuation, stopwords, small words.
        sentence = sentences[i].split()
        x = [word.strip(string.punctuation).lower() for word in sentence]
        x = [word for word in x if word not in stopwords.words('english')
             and word.isalpha() and len(word) > 1]  # NOTE: this removes hyphenated words and contractions
        # if x is not an empty array of words, add its words to processed
        if x:
            processed += x

    return processed


settings = {'word_dim': 15, 'learning_rate': .001, 'epochs': 500, 'window_size': 2}

file = open("gatsby.txt")
corpus = preprocessing(file.read())

w2v = word2vec()
w2v.prep_for_training()
w2v.initial_analysis()
w2v.train()
