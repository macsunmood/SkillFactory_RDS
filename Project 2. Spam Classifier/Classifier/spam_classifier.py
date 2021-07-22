import pandas as pd
import re
import string
import numpy as np

class NaiveBayesSpamFilter():
    def __init__(self, spam_dataset='spam_or_not_spam.csv'):
        self.pA = 0  # probability of encountering SPAM
        self.pNotA = 0  # probability of encountering NOT SPAM
        self.wordsDict = {'SPAM': {}, 'NOT_SPAM': {}}  # storage for spam- and nonspam-words
        self.totals = {'SPAM': 0, 'NOT_SPAM': 0}  # total counts for positives and for negatives
        self.data = pd.read_csv(spam_dataset).dropna()  
        
    def preprocess(self, body):
        body = ''.join([char for char in body if char not in string.punctuation])
        for r in ((r'\d', 'number '), (r'\b\w{1,3}\b ', '')):
            body = re.sub(*r, body.lower())
        return body

    def calculate_word_frequencies(self, body, label):
        body = self.preprocess(body)
        for word in body.split():
            self.wordsDict[label][word] = self.wordsDict.get(word, 0) + 1
            self.totals[label] += 1

    def train(self, X=None, y=None):
        if X is None and y is None:
            X = self.data['email']
            y = self.data['label'].apply(lambda x: 'SPAM' if x == 1 else 'NOT_SPAM')

        spam_count = 0
        for i in X.index:
            body, label = X.loc[i], y.loc[i]
            self.calculate_word_frequencies(body, label)
            if label == 'SPAM':
                spam_count += 1

        total = len(X.index)
        self.pA = spam_count / total
        self.pNotA = (total - spam_count) / total

    def calculate_P_Bi_A(self, word, label):
        # P(Bi|A) - probability of encountering a word
        return (self.wordsDict[label].get(word, 0) + 1) / self.totals[label]

    def calculate_P_B_A(self, text, label):
        # P(B|A) - probability of encountering a text
        PBA = 1.0
        for word in text.split():
            PBA *= self.calculate_P_Bi_A(word, label)
        return PBA

    def classify(self, email):
        if 0 in self.totals.values():
            return 'ERROR: Not enough train data or model training failed!'

        email = self.preprocess(email)

        isSpam = self.pA * self.calculate_P_B_A(email, 'SPAM')
        isNotSpam = self.pNotA * self.calculate_P_B_A(email, 'NOT_SPAM')
        
        return 'SPAM' if isSpam > isNotSpam else 'NOT_SPAM'