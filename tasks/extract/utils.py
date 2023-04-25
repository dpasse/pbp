from typing import List

import re
from nltk import pos_tag
from nltk.tokenize import word_tokenize

from extr.entities import EntityExtractor
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

    return text

def make_crf_dataset(dataset: List[str], entitiy_patterns):
    entity_extractor = EntityExtractor(entitiy_patterns)
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
