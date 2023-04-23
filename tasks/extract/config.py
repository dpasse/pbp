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
        label='PLAYER',
        regexes=[
            RegEx(expressions=[
                r'\b[A-Z]\.[A-Z][A-Za-z]+?\b',
                r'\b[A-Z]\.[A-Z][A-Za-z][.-]\s?[A-Z][a-z]+?\b',
            ]),
        ]
    ),
    RegExLabel(
        label='DISTANCE',
        regexes=[
            RegEx(expressions=[
                r'(?<=\s)(-?\d+\s+yards?)(?=\b)'
            ]),
        ]
    ),
    RegExLabel(
        label='POSITION',
        regexes=[
            RegEx(
                expressions=[
                    r'\b(WR|TE|RB|QB|)\b'
                ],
            ),
        ],
    ),
    RegExLabel(
        label='TEAM',
        regexes=[
            RegEx(
                expressions=[
                    r'\b[A-Z]{2,3}\b'
                ],
                skip_if=[
                    r'\b(II|AJ|TWO|YAC)\b'
                ]
            ),
        ],
    ),
    RegExLabel(
        label='SPOT',
        regexes=[
            RegEx(expressions=[
                r'\d{1,3}(?=\b)',
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
        .build(),
    RegExRelationLabelBuilder('is_at') \
        .add_e1_to_e2(
            e1='SPOT',
            relation_expressions=[
                r'\s',
            ],
            e2='TEAM',
        ) \
        .build()
]
