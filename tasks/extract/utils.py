import re


def transform_document(document: str) -> str:
    text = document[:]

    text = re.sub(
        r'(\w)(-)([A-Z][a-z]*\.[A-Z])',
        r'\1 \2 \3',
        text
    )

    return text
