from typing import List

from extr.regexes import SlimRegEx, RegEx, RegExLabel
from extr.relations import RegExRelationLabelBuilder


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
                r'\b[A-Z][a-z]*\.[A-Z][A-Za-z]+?\b',
                r'\b[A-Z][a-z]*\.[A-Z][A-Za-z]*[.-][A-Z][a-z]+?\b',
                r'\b[A-Z][a-z]*\.[A-Z][A-Za-z]* [A-Z][a-z]+?\b',
                r'\b[A-Z][a-z]+ [A-Z][a-z]+(?= Pass From)',
                r'(?<=Pass From )[A-Z][a-z]+ [A-Z][a-z]+(?= for\b)',
                r'\b[A-Z][a-z]+ [A-Z][a-z]+(?= -?\d+ Yd Rush)',

                ## really specific
                r'\b[AE]\.St\. Brown\b',
            ]),
        ]
    ),
    RegExLabel(
        label='DISTANCE',
        regexes=[
            RegEx(expressions=[
                r'(?<=\s)-?\d+\s+(yards?|Yds?)(?=\b)'
            ]),
        ]
    ),
    RegExLabel(
        label='POSITION',
        regexes=[
            RegEx(
                expressions=[
                    r'\b(WR|TE|RB|QB)\b'
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
                    SlimRegEx([r'\b(II|AJ|TWO|YAC)\b'])
                ]
            ),
        ],
    ),
    RegExLabel(
        label='SPOT',
        regexes=[
            RegEx(expressions=[
                r'-?\d{1,3}(?=\b)',
                r'(?<=\sto\s)-?\d{1,3}(?=\s)',
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
    RegExRelationLabelBuilder('spot_of_ball') \
        .add_e1_to_e2(
            e1='TEAM',
            relation_expressions=[
                r'\s+',
            ],
            e2='SPOT',
        ) \
        .build()
]
