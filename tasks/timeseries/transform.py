from typing import List

import nltk
import json
from collections import defaultdict

from extr import Entity, Relation
from extr.entities import create_entity_extractor, \
                          KnowledgeBaseEntityLinker, \
                          EntityAnnotator
from extr.relations import RelationExtractor
from extr.entities.context import ConText

from labels.entity_patterns import patterns
from labels.kb import kb as kb_patterns
from labels.relation_patterns import relation_patterns
from rules.context import rule_grouping
from knowledge.kb import kb, reversed_kb_mappings


entity_extractor = create_entity_extractor(patterns, kb_patterns)

entity_annotator = EntityAnnotator()
relation_extractor = RelationExtractor(relation_patterns)

conText = ConText(
    rule_grouping=rule_grouping,
    word_tokenizer=nltk.tokenize.word_tokenize
)

entity_linker = KnowledgeBaseEntityLinker(
    attribute_label='concepts',
    kb=kb
)

def extract_data(text: str):
    entities = entity_extractor.get_entities(text)
    entities = entity_linker.link(entities)
    entities = conText.apply(
        text,
        entities,
        filter_out_rule_labels=True
    )
    
    relations = relation_extractor.extract(
        entity_annotator.annotate(text, entities),
        entities
    )

    return entities, relations

def extract_and_group_data_by_moment(instances: List[str]):
    group_by_quarter = defaultdict(list)
    for instance in instances:
        entities, relations = extract_data(instance)

        observation = {
            'entities': entities,
        }

        for relation in relations:
            definition = relation.definition
            if not definition in observation:
                observation[definition] = []

            observation[definition].append(relation)

        if not 'r("QUARTER", "TIME")' in observation:
            continue

        is_at = observation['r("QUARTER", "TIME")'][0]
        e1 = is_at.e1
        e2 = is_at.e2

        group_by_quarter[f'{e1.text}-{e2.text}'].append(observation)

    return list(group_by_quarter.values())

def get_events(entities: List[Entity]):
    data = set()
    events = (
        entity for entity in entities if entity.label=='EVENT'
    )

    for event in events:
        negated = event.is_a('ctypes', 'NEGATED')
        for concept in event.get_attributes_by_label('concepts'):
            key = reversed_kb_mappings[concept]
            if negated:
                key = f'NEGATED: {key}'

            data.add(key)

    return list(data)

def get_formations(entities: List[Entity]):
    data = set()
    formations = (
        entity for entity in entities if entity.label=='FORMATION'
    )

    for formation in formations:
        for concept in formation.get_attributes_by_label('concepts'):
            data.add(reversed_kb_mappings[concept])

    return list(data)

def get_players(entities: List[Entity]):
    data = set(
        [
            entity.text for entity in entities if entity.label=='PLAYER'
        ]
    )

    return list(data)


def get_data_from_entities(entities: List[Entity]):
    return {
        'events': get_events(entities),
        'formations': get_formations(entities),
        'players': get_players(entities),
    }

def get_quarter_and_time(is_at: Relation):
    e1 = is_at.e1
    concept_id = list(
        e1.get_attributes_by_label('concepts')
    )[0]

    quarter = reversed_kb_mappings[concept_id]
    return quarter, is_at.e2.text

def get_side_and_spot_of_ball(is_spot_of_ball: Relation):
    e1 = is_spot_of_ball.e1
    e2 = is_spot_of_ball.e2

    return e1.text, int(e2.text)

def get_info(relation: Relation):
    return f'{relation.e1.text}-{relation.e2.text}'

def build_timeline(observations):
    timeline = []
    previous_spot_of_ball = []
    for event_id, group_by_quarter_datas in enumerate(observations):
        for parsed_data in group_by_quarter_datas:
            spot_of_ball = previous_spot_of_ball \
                if not 'r("TEAM", "QUANTITY")' in parsed_data \
                else parsed_data['r("TEAM", "QUANTITY")']

            if len(spot_of_ball) == 0:
                continue

            ## cache previous, apply if missing on next record
            previous_spot_of_ball = spot_of_ball

            quarter, time = get_quarter_and_time(
                parsed_data['r("QUARTER", "TIME")'][0]
            )
            
            data = {
                'event': event_id + 1,
                'quarter': quarter,
                'time': time,
                'spots': [],
                'info': []
            }

            data.update(
                get_data_from_entities(parsed_data['entities'])
            )

            info_relation_mapper = [
                ('r("EVENT", "TEAM")', get_info),
                ('r("EVENT", "PLAYER")', get_info)
            ]

            for key, method in info_relation_mapper:
                if key in parsed_data:
                    data['info'].extend(
                        list(map(method, parsed_data[key]))
                    )

            for side, at in map(get_side_and_spot_of_ball, spot_of_ball):
                data['spots'].append({
                    'side': side,
                    'at': at,
                })

            timeline.append(data)

    return timeline

def transform():
    instances = []
    with open('./2022_W1_NYJ_BLT.txt', 'r') as source_file:
        instances = source_file.read().split('\n')

    observations = extract_and_group_data_by_moment(instances)
    timeline = build_timeline(observations)

    with open('./2022_W1_NYJ_BLT_TS.json', 'w') as output_file:
        output_file.write(
            json.dumps(timeline, indent=2)
        )

if __name__ == '__main__':
    transform()