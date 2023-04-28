from typing import List

import re
from nltk import pos_tag
from nltk.tokenize import word_tokenize

from extr.entities import create_entity_extractor
from extr_ds.labelers import IOB


def sentence_tokenizer(text: str) -> List[str]:
    return [
        word_tokenize(text)
    ]

def transform_document(document: str) -> str:
    text = document[:]

    text = re.sub(
        r'(\w)(-)([A-Z][a-z]*\.[A-Z])',
        r'\1 \2 \3',
        text
    )

    text = re.sub(
        r'\b(\d+)(-)([A-Z])',
        r'\2 \3',
        text
    )

    text = re.sub(
        r'\b(\d+)([A-Z]\.)',
        r'\1 \2',
        text
    )

    text = re.sub(
        r'(injured during the play\.)',
        r'\1 ',
        text
    )

    text = re.sub(r' +', ' ', text)

    return text

def make_crf_dataset(dataset: List[str], entitiy_patterns, kb=None):
    entity_extractor = create_entity_extractor(entitiy_patterns, kb)
    labeler = IOB(sentence_tokenizer, entity_extractor)
    
    train_set = []
    for i, row in enumerate(dataset):
        text = transform_document(row)

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
