from typing import List

import re
from nltk.tokenize import word_tokenize


def word_tokenizer(text: str) -> List[str]:
    return word_tokenize(text)

def transform_text(document: str) -> str:
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