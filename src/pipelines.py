def identity(words):
    return words

w = 50 # The weight for the positive class


# ValueError: blocks[0,:] has incompatible row dimensions. Got blocks[0,1].shape[0] == 1, expected 1200.
model2 = Pipeline([
    ('preprocess_union', FeatureUnion([
    		('term_freq_feature', Pipeline([
    			('normalizer', GildPreprocessor()),
    			('vectorizer', TfidfVectorizer(tokenizer=identity, preprocessor=None, lowercase=False))
    			])),
    		('length_feature', LengthAnalyzer())
    	])),
    ('trees', RandomForestClassifier(random_state=0, n_jobs=-1, class_weight={0: 1, 1: w}))
])


#TypeError: can't multiply sequence by non-int of type 'float'
model2 = Pipeline([
    ('preprocess_union', FeatureUnion(
    	transformer_list = [
    		('term_freq_feature', Pipeline([
    			('normalizer', GildPreprocessor()),
    			('vectorizer', TfidfVectorizer(tokenizer=identity, preprocessor=None, lowercase=False))
    			])),
    		('length_feature', LengthAnalyzer())
    	],
    	transformer_weights = { #TypeError: can't multiply sequence by non-int of type 'float'
    		'term_freq_feature': 0.6,
    		'length_feature': 0.4
    	}
    	)),
    ('trees', RandomForestClassifier(random_state=0, n_jobs=-1, class_weight={0: 1, 1: w}))
])


w = 50 # The weight for the positive class

model = Pipeline([
    ('normalizer', GildPreprocessor()),
    ('vectorizer', TfidfVectorizer(tokenizer=identity, preprocessor=None, lowercase=False)),
    ('trees', RandomForestClassifier(random_state=0, n_jobs=-1, class_weight={0: 1, 1: w}))
])

model = Pipeline([
    ('normalizer', GildPreprocessor()),
    ('vectorizer', TfidfVectorizer(tokenizer=identity, preprocessor=None, lowercase=False)),
    ('bayes', MultinomialNB()),
])