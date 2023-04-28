from typing import List, Set, Dict
import os
import re
import json

from utils import transform_document
from filesystem import get_data
from config import entitiy_patterns, kb
from extr.entities import create_entity_extractor, LabelOnlyEntityAnnotator


annotator = LabelOnlyEntityAnnotator()
entity_extractor = create_entity_extractor(entitiy_patterns, kb)


def save_data(dataset: List[str], file_path: str) -> None:
    with open(file_path, 'w') as dev:
        dev.write('\n'.join(dataset))

def annotate(in_file: str, entities_out_file: str):
    dataset = get_data(
        os.path.join('..', 'data', '3', in_file + '.txt')
    )

    text_annotations: List[str] = []
    extracted_text_by_label: Dict[str, Set[str]] = {}
    for row in dataset:
        text = transform_document(row)

        entities = entity_extractor.get_entities(text)
        annotation_result = annotator.annotate(text, entities)
        text_annotations.append(
            annotation_result.annotated_text
        )

        for entity in entities:
            if not entity.label in extracted_text_by_label:
                extracted_text_by_label[entity.label] = set()

            extracted_text_by_label[entity.label].add(entity.text)

    save_data(
        text_annotations,
        os.path.join('..', 'data', '4', entities_out_file + '.txt')
    )

    redacted_templates = set()
    redacted_templates_file_path = os.path.join('..', 'data', '5', entities_out_file + '-redacted.txt')
    if os.path.exists(redacted_templates_file_path):
        redacted_templates = set(
            get_data(redacted_templates_file_path)
        )

    redacted_dataset = [
        row
        for _, row in (
            (i, re.sub(' +', ' ', re.sub(r'<[A-Z]+>.+?</[A-Z]+>', ' ', row)))
            for i, row
            in enumerate(text_annotations)
        )
        if not row in redacted_templates
    ]

    save_data(
        redacted_dataset,
        os.path.join('..', 'data', '4', entities_out_file + '-redacted.txt')
    )

    for key, value in extracted_text_by_label.items():
        extracted_text_by_label[key] = list(sorted(value))

    stats_path = os.path.join('..', 'data', '4', 'dev-ents.stats.json')
    with open(stats_path, 'w') as dev_stats:
        dev_stats.write(json.dumps(extracted_text_by_label, indent=2))


if __name__ == '__main__':
    annotate(
        'dev',
        'dev-ents',
    )
