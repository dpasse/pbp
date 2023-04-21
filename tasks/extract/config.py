from typing import List
from extr import RegEx, RegExLabel, RegExRelationLabelBuilder


entitiy_patterns: List[RegExLabel] = [
    RegExLabel(
        label='TIME',
        regexes=[
            RegEx(expressions=[
                r'\b[0-9]{1,2}:[0-9]{2}\b',
            ]),
        ],
    ),
    RegExLabel(
        label='PERIOD',
        regexes=[
            RegEx(expressions=[
                r'\b(1st|2nd|3rd|4th|OT)\b',
            ]),
        ]
    )
]

relation_patterns = [
    RegExRelationLabelBuilder('is_at') \
        .add_e2_to_e1(
            e2='TIME',
            relation_expressions=[
                r'(\s-\s)',
            ],
            e1='PERIOD'
        ) \
        .build()
]
