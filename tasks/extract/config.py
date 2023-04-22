from typing import List
import re
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
    ),
    RegExLabel(
        label='EVENT',
        regexes=[
            RegEx(
                expressions=[
                    r'\b(kicks|kneels|pass|run|sacked|scrambles)\b',
                ],
                flags=re.IGNORECASE
            ),
        ]
    ),
    RegExLabel(
        label='PLAYER',
        regexes=[
            RegEx(expressions=[
                r'\b[A-Z]\.[A-Z][A-Za-z]+?\b',
            ]),
        ]
    ),
    RegExLabel(
        label='DISTANCE',
        regexes=[
            RegEx(expressions=[
                r'(?<=\s)(-?\d+\s+yards)(?=\b)'
            ]),
        ]
    ),
    RegExLabel(
        label='SPOT',
        regexes=[
            RegEx(expressions=[
                r'(?<=\s)[A-Z]{2,}\s+\d{1,3}(?=\s)',
                r'(?<=\sto\s)\d{1,3}(?=\s)',
            ])
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
