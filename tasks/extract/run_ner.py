import os

import sklearn_crfsuite
from sklearn_crfsuite import metrics

from config import entitiy_patterns, kb
from features import sent2features, sent2labels
from utils import make_crf_dataset
from filesystem import get_data
from sklearn.model_selection import train_test_split
from extr_ds.validators import check_for_differences


def annotate(in_file: str):
    train_sents = make_crf_dataset(
        get_data(os.path.join('..', 'data', '5', in_file + '.txt')),
        entitiy_patterns,
        kb
    )

    X = [sent2features(s) for s in train_sents]
    y = [sent2labels(s) for s in train_sents]

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=.15)

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

    y_pred = crf.predict(X_train)

    print(
        metrics.flat_f1_score(y_train, y_pred, average='weighted', labels=labels)
    )

    for i, outcomes in enumerate(zip(y_pred, y_train)):
        differences = check_for_differences(outcomes[1], outcomes[0])
        if differences.has_diffs:
            print(i)
            for diff in differences.diffs_between_labels:
                print(X_train[i][diff.index])
                print(diff.diff_type)
                print()

    y_test_pred = crf.predict(X_test)

    print(
        metrics.flat_f1_score(y_test, y_test_pred, average='weighted', labels=labels)
    )

    for i, outcomes in enumerate(zip(y_test_pred, y_test)):
        differences = check_for_differences(outcomes[1], outcomes[0])
        if differences.has_diffs:
            print(i)
            for diff in differences.diffs_between_labels:
                print(X_test[i][diff.index]['word.lower()'])
                print(diff.diff_type)
                print(outcomes[1][diff.index], outcomes[0][diff.index])
                print()


if __name__ == '__main__':
    annotate('dev')
