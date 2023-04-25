from typing import List
import os

import sklearn_crfsuite
from sklearn_crfsuite import metrics

from features import sent2features, sent2labels
from utils import transform_document
from nltk.tokenize import word_tokenize
from nltk import pos_tag
from config import entitiy_patterns
from extr.entities import EntityExtractor
from extr_ds.labelers import IOB

def sentence_tokenizer(text: str) -> List[str]:
    return [
        word_tokenize(text)
    ]

entity_extractor = EntityExtractor(entitiy_patterns)
labeler = IOB(sentence_tokenizer, entity_extractor)

def make_dataset(file_path: str):
    def get_data(file_path: str) -> List[str]:
        dataset = []
        with open(file_path, 'r') as dev:
            dataset = dev.read().split('\n')

        return dataset
    
    train_set = []
    for i, row in enumerate(get_data(file_path)):
        text = transform_document(row)

        try:
            observation = list(labeler.label(text))[0]
            tokens = list(map(lambda a: a.text, observation.tokens))
            pos = list(map(lambda a: a[1], pos_tag(tokens)))
            labels = observation.labels

            assert len(tokens) == len(pos) and len(tokens) == len(labels)
        except:
            print(text)
            print(i+1)
            print(sentence_tokenizer(text))

            raise

        train_set.append(list(zip(tokens, pos, labels)))

    return train_set

def annotate(in_file: str):
    train_sents = make_dataset(
        os.path.join('..', 'data', '3', in_file + '.txt')
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
