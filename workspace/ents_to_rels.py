from typing import Any, Dict, List

from extr import Entity, Location, Relation
from extr.entities import AbstractEntityExtractor
from extr.relations import AbstractRelationExtractor
from extr_ds.labelers.relation import RelationLabeler, RelationBuilder, BaseRelationLabeler, RelationClassification
from extr_ds.models import RelationLabel
from extr.relations import RelationAnnotatorWithEntityType
from transformers import logging, \
                         pipeline

logging.set_verbosity_error()

ner_model_output_checkpoint = 'transformers/nfl_pbp_token_classifier'
re_model_output_checkpoint = 'transformers/nfl_pbp_relation_classifier'

class TransformerEntityExtractor(AbstractEntityExtractor):
    def __init__(self, model_output_checkpoint: str, threshold: float=.5) -> None:
        self._threshold = threshold
        self._classifier = pipeline(
            'ner', 
            model=model_output_checkpoint,
            aggregation_strategy='simple'
        )

    def get_entities(self, text: str) -> List[Entity]:
        entities = []
        for response in filter(lambda r: r['score'] >= self._threshold, self._classifier(text)):
            location = Location(start=response['start'], end=response['end'])
            entities.append(
                Entity(
                    identifier=len(entities) + 1,
                    label=response['entity_group'],
                    text=location.extract(text),
                    location=location
                )
            )

        return entities

class TransformationRelationLabeler(BaseRelationLabeler):
    def __init__(self,
                 model_output_checkpoint: str,
                 relation_builder: RelationBuilder,
                 threshold: float=.5
    ):
        super().__init__(relation_builder)

        self._classifier = pipeline(
            'text-classification', 
            model=model_output_checkpoint
        )

        self._threshold = threshold

    def label(self, text: str, entities: List[Entity]) -> List[RelationLabel]:
        relation_labels = super().label(text, entities)
        responses = self._classifier(
            list(map(lambda label: label.sentence, relation_labels))
        )

        labels = []
        for relation_label, response in zip(relation_labels, responses):
            if response['score'] >= self._threshold:
                relation = relation_label.relation
                relation_label.relation = Relation(
                    response['label'],
                    e1=relation.e1,
                    e2=relation.e2
                )

            labels.append(relation_label)

        return labels
        

def run():
    text = '(6:51 - 1st) (Shotgun) P.Mahomes scrambles right end to LAC 34 for 2 yards (S.Joseph; K.Van Noy). FUMBLES (S.Joseph), and recovers at LAC 34.'

    classifier = RelationClassification(
        TransformerEntityExtractor(ner_model_output_checkpoint),
        TransformationRelationLabeler(
            re_model_output_checkpoint,
            relation_builder=RelationBuilder([
                ('TEAM', 'QUANTITY', 'NO_RELATION')
            ]),
        ),
    )

    relation_labels = classifier.label(text)
    for relation_label in relation_labels:
        print(relation_label)

    print()
    print()

    for relation_label in filter(lambda a: a.label != 'NO_RELATION', relation_labels):
        print(relation_label)
        
if __name__ == '__main__':
    run()
