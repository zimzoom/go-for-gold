import numpy as np
import pandas as pd
import string
import re
from nltk.tokenize import word_tokenize, wordpunct_tokenize, RegexpTokenizer
from nltk.stem.snowball import SnowballStemmer
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, confusion_matrix, recall_score, roc_auc_score, accuracy_score



# Identity function can be passed as parameter to not do any processing (as in TfidfVectorizer)
def identity(words):
    return words

# Print report of performance metrics for model.
# Call this after fitting model.
def model_report(model, X_test, y_test):
    pred = model.predict(X_test)
    print(classification_report(y_test, pred, digits=6))
    # Is our model predicting just one class?
    print( "Classes predicted:  ", np.unique( pred ) )

    # How's our accuracy?
    print( "Accuracy:  ", accuracy_score(y_test, pred) )

    # What about AUROC?
    prob_y = model.predict_proba(X_test)
    prob_y = [p[1] for p in prob_y]
    print( "ROC AUC Score:  ", roc_auc_score(y_test, prob_y) )

    tn, fp, fn, tp = confusion_matrix(y_test, pred).ravel()
    print("True Pos: ", tp, "False Pos: ", fp)
    print("FP to TP Ratio::  ", (fp/tp))
    print("True Neg: ", tn, "False Neg: ", fn)


def create_pipeline(estimator, reduction=False):

    steps = [
        ('normalize', TextNormalizer()),
        ('vectorize', TfidfVectorizer(
            tokenizer=identity, preprocessor=None, lowercase=False
        ))
    ]

    if reduction:
        steps.append((
            'reduction', TruncatedSVD(n_components=10000)
        ))

    # Add the estimator
    steps.append(('classifier', estimator))
    return Pipeline(steps)


def snowtokenize(text):
    stem = nltk.stem.SnowballStemmer('english')
    text = text.lower()

    for token in nltk.word_tokenize(text):
        if token in string.punctuation: continue
        yield stem.stem(token)


def regtokenize(doc):
    tokenizer = RegexpTokenizer(r'\w+')
    tokens = tokenizer.tokenize(doc.lower())
    return tokens