w = 50 # The weight for the positive (minority) class


# With word count & subjectivity score feature
model4 = Pipeline([
    ('preprocess_union', FeatureUnion([
            ('term_freq_feature', Pipeline([
                ('normalizer', GildPreprocessor()),
                ('vectorizer', TfidfVectorizer(tokenizer=identity, preprocessor=None, lowercase=False))
                ])),
            ('word_counter', WordCounterSubjectivity())
        ])),
    ('trees', RandomForestClassifier(random_state=0, n_jobs=-1, class_weight={0: 1, 1: w}))
])


# With word count feature
model3 = Pipeline([
    ('preprocess_union', FeatureUnion([
            ('term_freq_feature', Pipeline([
                ('normalizer', GildPreprocessor()),
                ('vectorizer', TfidfVectorizer(tokenizer=identity, preprocessor=None, lowercase=False))
                ])),
            ('word_counter', WordCounter())
        ])),
    ('trees', RandomForestClassifier(random_state=0, n_jobs=-1, class_weight={0: 1, 1: w}))
])


model2 = Pipeline([
    ('normalizer', GildPreprocessor()),
    ('vectorizer', TfidfVectorizer(tokenizer=identity, preprocessor=None, lowercase=False)),
    ('trees', RandomForestClassifier(random_state=0, n_jobs=-1, class_weight={0: 1, 1: w}))
])


model1 = Pipeline([
    ('normalizer', GildPreprocessor()),
    ('vectorizer', TfidfVectorizer(tokenizer=identity, preprocessor=None, lowercase=False)),
    ('trees', RandomForestClassifier(random_state=0, n_jobs=-1, class_weight='balanced'))
])


model = Pipeline([
    ('normalizer', GildPreprocessor()),
    ('vectorizer', TfidfVectorizer(tokenizer=identity, preprocessor=None, lowercase=False)),
    ('bayes', MultinomialNB()),
])