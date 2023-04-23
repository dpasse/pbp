from typing import List, Set, Dict
import os
import json

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

    text_annotations: List[str] = []
    extracted_text_by_label: Dict[str, Set[str]] = {}
    for row in dataset:
        entities = entity_extractor.get_entities(row)
        text_annotations.append(
            annotator.annotate(row, entities).annotated_text
        )

        for entity in entities:
            if not entity.label in extracted_text_by_label:
                extracted_text_by_label[entity.label] = set()

            extracted_text_by_label[entity.label].add(entity.text)

    save_data(
        text_annotations,
        os.path.join('..', 'data', '4', out_file)
    )

    for key, value in extracted_text_by_label.items():
        extracted_text_by_label[key] = list(sorted(value))

    with open(os.path.join('..', 'data', '4', 'dev.stats.json'), 'w') as dev_stats:
        dev_stats.write(json.dumps(extracted_text_by_label, indent=2))


if __name__ == '__main__':
    annotate('dev.txt', 'dev.txt')
