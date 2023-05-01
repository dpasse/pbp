from typing import List

import os

import sklearn_crfsuite
from sklearn_crfsuite import metrics

from nltk import pos_tag

from labels import entity_patterns, kb
from models.features import sent2features, sent2labels
from utils import transform_text, sentence_tokenizer
from sklearn.model_selection import train_test_split
from extr_ds.validators import check_for_differences

from extr.entities import create_entity_extractor
from extr_ds.labelers import IOB
from extr_ds.manager.utils.filesystem import load_data


def make_crf_dataset():
    entity_extractor = create_entity_extractor(entity_patterns, kb)
    labeler = IOB(sentence_tokenizer, entity_extractor)
    
    train_set = []
    for i, row in enumerate(load_data(os.path.join('4', 'ents.txt'))):
        text = transform_text(row)

        try:
            for observation in labeler.label(text):

                tokens = list(map(lambda a: a.text, observation.tokens))
                labels = observation.labels

                assert len(tokens) == len(labels)

                train_set.append(
                    list(
                        zip(
                            tokens,
                            list(map(lambda a: a[1], pos_tag(tokens))),
                            labels
                        )
                    )
                )
        except:
            print('text:', text)
            print('row#:', i+1)
            print('tokens:', sentence_tokenizer(text))

            raise

    return train_set

def run_model():
    train_sents = make_crf_dataset()

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
        'X_train:',
        metrics.flat_f1_score(y_train, y_pred, average='weighted', labels=labels)
    )

    for i, outcomes in enumerate(zip(y_pred, y_train)):
        differences = check_for_differences(outcomes[1], outcomes[0])
        if differences.has_diffs:
            for diff in differences.diffs_between_labels:
                print(i, X_train[i][diff.index], '-', diff.diff_type)
                print()

    y_test_pred = crf.predict(X_test)

    print(
        'X_test:',
        metrics.flat_f1_score(y_test, y_test_pred, average='weighted', labels=labels)
    )

    print()

    for i, outcomes in enumerate(zip(y_test_pred, y_test)):
        differences = check_for_differences(outcomes[1], outcomes[0])
        if differences.has_diffs:
            for diff in differences.diffs_between_labels:
                print(X_test[i][diff.index]['word.lower()'], '-', diff.diff_type)
                print('s1:', outcomes[1][diff.index], 'vs s2:', outcomes[0][diff.index])
                print()


if __name__ == '__main__':
    run_model()
