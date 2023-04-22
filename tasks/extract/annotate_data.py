from typing import List
import os

from config import entitiy_patterns
from extr.entities import EntityExtractor, LabelOnlyEntityAnnotator


annotator = LabelOnlyEntityAnnotator()
entity_extractor = EntityExtractor(entitiy_patterns)

def get_data(file_path: str) -> List[str]:
    dataset = []
    with open(file_path, 'r') as dev:
        dataset = dev.read().split('\n')

    return dataset

def save_data(dataset: List[str], file_path: str) -> None:
    with open(file_path, 'w') as dev:
        dev.write('\n'.join(dataset))


def annotate(in_file: str, out_file: str):
    dataset = get_data(
        os.path.join('..', 'data', '3', in_file)
    )

    annotations = []
    for row in dataset:
        entities = entity_extractor.get_entities(row)
        annotations.append(
            annotator.annotate(row, entities).annotated_text
        )

    save_data(
        annotations,
        os.path.join('..', 'data', '4', out_file)
    )


if __name__ == '__main__':
    annotate('dev.txt', 'dev.txt')
