from typing import List
import os

import sklearn_crfsuite
from sklearn_crfsuite import metrics

from config import entitiy_patterns
from features import sent2features, sent2labels
from utils import make_crf_dataset
from filesystem import get_data


def annotate(in_file: str):
    train_sents = make_crf_dataset(
        get_data(os.path.join('..', 'data', '3', in_file + '.txt')),
        entitiy_patterns
    )

    X_train = [sent2features(s) for s in train_sents]
    y_train = [sent2labels(s) for s in train_sents]

    crf = sklearn_crfsuite.CRF(
        algorithm='lbfgs',
        c1=0.1,
        c2=0.1,
        max_iterations=100,
        all_possible_transitions=True
    )
    
    crf.fit(X_train, y_train)

    labels = list(crf.classes_)
    labels.remove('O')
    labels

    y_pred = crf.predict(X_train)

    print(
        metrics.flat_f1_score(y_train, y_pred, average='weighted', labels=labels)
    )


if __name__ == '__main__':
    annotate('dev')
