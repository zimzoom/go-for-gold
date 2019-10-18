import string
from nltk.corpus import stopwords
from nltk.corpus import wordnet
from nltk import wordpunct_tokenize
from nltk import WordNetLemmatizer
from nltk import sent_tokenize
from nltk import pos_tag
from sklearn.base import BaseEstimator, TransformerMixin


# Identity function can be passed as parameter to not do any processing (as in TfidfVectorizer)
def identity(words):
    return words


class GildPreprocessor(BaseEstimator, TransformerMixin):
    '''
    For normalizing reddit comments to classify whether comments are gilded or not.
    - tokenizes
    - (optionally) strips punctuation and makes all lowercase
    - filters out stopwords
    - filters out words commonly found in edits made to gilded comments after the fact
    - lemmatizes
    '''
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


class WordCounterSubjectivity(BaseEstimator, TransformerMixin):
    '''
    Analyzes comment length by word count.
    Also calculates a "subjectivity score" based on use of "I", "me", etc.
    '''
    def __init__(self):
        self.subj_toks = ["i", "me", "ive", "im", "my", "mine"]
        return None
        
    def fit(self, X, y=None):
        return self

    def transform(self, X):
        word_counts = np.array([
            len((self.simplify_text(doc)).split()) for doc in X
        ])
        subj_scores = np.array([
            self.subjectivity_score(doc, word_counts[i]) for i, doc in enumerate(X)
        ])
        word_counts = word_counts.reshape(-1, 1)
        subj_scores = subj_scores.reshape(-1, 1)
        return np.hstack((word_counts, subj_scores))
    
    def simplify_text(self, doc):
        clean1 = re.sub(r'['+string.punctuation + '’—”'+']', "", doc.lower())
        clean2 = re.sub(r'\W+', ' ', clean1)
        return clean2

    def subjectivity_score(self, doc, wc):
        subj_counter = 0
        for word in self.simplify_text(doc):
            if word in self.subj_toks:
                subj_counter += 1
        return subj_counter/wc


class WordCounter(BaseEstimator, TransformerMixin):
    '''
    Analyzes comment length by word count.
    '''
    def __init__(self):
        return None
        
    def fit(self, X, y=None):
        return self

    def transform(self, X):
        Z = np.array([
            self.count_text(doc) for doc in X
        ])
        return Z.reshape(-1, 1)
    
    def count_text(self, doc):
        clean1 = re.sub(r'['+string.punctuation + '’—”'+']', "", doc.lower())
        clean2 = re.sub(r'\W+', ' ', clean1)
        return len(clean2.split())
