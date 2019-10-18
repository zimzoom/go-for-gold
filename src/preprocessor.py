import string
from nltk.corpus import stopwords
from nltk.corpus import wordnet
from nltk import wordpunct_tokenize
from nltk import WordNetLemmatizer
from nltk import sent_tokenize
from nltk import pos_tag
from sklearn.base import BaseEstimator, TransformerMixin

class GildPreprocessor(BaseEstimator, TransformerMixin):

    def __init__(self,
                 lower=True, strip=True):
        self.lower      = lower
        self.strip      = strip
        self.stopwords  = set(stopwords.words('english'))
        self.punct      = set(string.punctuation)
        self.lemmatizer = WordNetLemmatizer()
        self.gildwords  = ["thanks", "gold", "gilded", "gild", "edit", "obligatory", "blew", "blown"]

    def fit(self, X, y=None):
        return self

    def transform(self, X):
        return [
            list(self.tokenize(doc)) for doc in X
        ]

    def tokenize(self, document):
        for sent in sent_tokenize(document):
            for token, tag in pos_tag(wordpunct_tokenize(sent)):
                token = token.lower() if self.lower else token
                token = token.strip() if self.strip else token
                token = token.strip('_') if self.strip else token
                token = token.strip('*') if self.strip else token

                if token in self.stopwords:
                    continue

                if token in self.gildwords:
                    continue

                if all(char in self.punct for char in token):
                    continue

                lemma = self.lemmatize(token, tag)
                yield lemma

    def lemmatize(self, token, tag):
        tag = {
            'N': wordnet.NOUN,
            'V': wordnet.VERB,
            'R': wordnet.ADV,
            'J': wordnet.ADJ
        }.get(tag[0], wordnet.NOUN)

        return self.lemmatizer.lemmatize(token, tag)
