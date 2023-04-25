from typing import List
import os

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

def get_data(file_path: str) -> List[str]:
    dataset = []
    with open(file_path, 'r') as dev:
        dataset = dev.read().split('\n')

    return dataset

def annotate(in_file: str):
    dataset = get_data(
        os.path.join('..', 'data', '3', in_file + '.txt')
    )

    train_set = []
    for i, row in enumerate(dataset):

        instances = []
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

        instances.append(
            list(zip(tokens, pos, labels))
        )

        train_set.append(instances)

    print(train_set[0])
        

if __name__ == '__main__':
    annotate('dev')
