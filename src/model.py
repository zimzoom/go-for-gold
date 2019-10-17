
class MyPreprocessor(BaseEstimator, TransformerMixin):

    def __init__(self,
                 lower=True, strip=True):
        self.lower      = lower
        self.strip      = strip
        self.stopwords  = set(sw.words('english'))
        self.punct      = set(string.punctuation)
        self.lemmatizer = WordNetLemmatizer()

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

                if all(char in self.punct for char in token):
                    continue

                lemma = self.lemmatize(token, tag)
                yield lemma

    def lemmatize(self, token, tag):
        tag = {
            'N': wn.NOUN,
            'V': wn.VERB,
            'R': wn.ADV,
            'J': wn.ADJ
        }.get(tag[0], wn.NOUN)

        return self.lemmatizer.lemmatize(token, tag)


def identity(words):
    return words

model = Pipeline([
    ('normalizer', MyPreprocessor()),
    ('vectorizer', TfidfVectorizer(tokenizer=identity, preprocessor=None, lowercase=False)),
    ('bayes', MultinomialNB()),
])