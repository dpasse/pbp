from typing import List, Set, Dict
import os
import json

from utils import transform_document
from filesystem import get_data
from config import entitiy_patterns, relation_patterns
from extr.entities import EntityExtractor, LabelOnlyEntityAnnotator, EntityAnnotator
from extr.relations import RelationExtractor, RelationAnnotator


annotator = LabelOnlyEntityAnnotator()
entity_extractor = EntityExtractor(entitiy_patterns)
relations_extractor = RelationExtractor(relation_patterns)
relation_annotator = RelationAnnotator()


def save_data(dataset: List[str], file_path: str) -> None:
    with open(file_path, 'w') as dev:
        dev.write('\n'.join(dataset))

def annotate(in_file: str, entities_out_file: str, relations_out_file: str):
    dataset = get_data(
        os.path.join('..', 'data', '3', in_file + '.txt')
    )

    text_annotations: List[str] = []
    relation_annotations: List[str] = []
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

        
        relations = relations_extractor.extract(
            EntityAnnotator().annotate(text, entities)
        )

        relation_annotations.extend(
            list(
                map(
                    lambda rel: f'{rel.label} | {relation_annotator.annotate(text, rel)}',
                    relations
                )
            )
        )

    save_data(
        text_annotations,
        os.path.join('..', 'data', '4', entities_out_file + '.txt')
    )

    save_data(
        relation_annotations,
        os.path.join('..', 'data', '4', relations_out_file + '.txt')
    )

    for key, value in extracted_text_by_label.items():
        extracted_text_by_label[key] = list(sorted(value))

    stats_path = os.path.join('..', 'data', '4', 'dev-ents.stats.json')
    with open(stats_path, 'w') as dev_stats:
        dev_stats.write(json.dumps(extracted_text_by_label, indent=2))


if __name__ == '__main__':
    annotate('dev', 'dev-ents', 'dev-rels')
