import re
from typing import List

from extr.regexes import SlimRegEx, RegEx, RegExLabel
from extr.relations import RegExRelationLabelBuilder


kb = {
    'PLAYER': [
        'A.St. Brown',
        'E.St. Brown',
        'D. McCourty',
        'T.J. Watt',
        'A.Van Ginkel',
        'Kenneth Walker III',
        'G.Van Roten',
        'K.Van Noy',
    ],
    'PERIOD': [
        '1st',
        '2nd',
        '3rd',
        '4th',
        'OT',
    ],
    'POSITION': [
        'WR',
        'RB',
        'TE',
        'QB',
        'Center',
        'Holder'
    ],
    'TEAM': [
        'ARZ',
        'ATL',
        'BLT',
        'BUF',
        'CAR',
        'CHI',
        'CIN',
        'CLV',
        'Cleveland',
        'DAL',
        'DEN',
        'DET',
        'GB',
        'Green Bay',
        'HST',
        'IND',
        'Indianapolis',
        'JAX',
        'KC',
        'Kansas City',
        'LA',
        'LAC',
        'LV',
        'Las Vegas',
        'MIA',
        'MIN',
        'Minnesota',
        'NE',
        'New England',
        'NO',
        'New Orleans',
        'NYG',
        'New York Giants',
        'NYJ',
        'New York Jets',
        'PHI',
        'PIT',
        'SEA',
        'SF',
        'TB',
        'TEN',
        'WAS',
        'Washington',
    ]
}

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
        label='PLAYER',
        regexes=[
            RegEx(expressions=[
                r'\b[A-Z][a-z]*\.[A-Z][\'A-Za-z]+\b',
                r'\b[A-Z][a-z]*\.[A-Z][A-Za-z]*[.-][A-Z][a-z]+\b',
                r'\b[A-Z][\'A-Za-z]+ ([A-Z][a-z]+|-)+(?= (?:[Pp]ass [Ff]rom|PAT ))',
                r'(?<=[Pp]ass [Ff]rom )[A-Z][a-z]+ [A-Z][a-z]+(?= (?:for\b|\())',
                r'\b[A-Z][\'A-Za-z]+ ([A-Z][a-z]+|-)+(?= -?\d+ Yd (?:[Rr]ush|(?:Interception|KO) Return|Run|[Pp]ass [Ff]rom))',
            ]),
        ]
    ),
    RegExLabel(
        label='FORMATION',
        regexes=[
            RegEx(
                expressions=[
                    r'\b(?:no huddle|shotgun)(?=\b)',
                    r'\b(?:pass|punt) formation(?=\b)'
                ],
                flags=re.IGNORECASE
            ),
        ]
    ),
    RegExLabel(
        label='DIRECTION',
        regexes=[
            RegEx(
                expressions=[
                    r'(?<=\b)(deep|short) (left|right|middle)(?=\b)',
                    r'(?<=\b)(left|right|middle)(?=\b)'
                ],
                flags=re.IGNORECASE
            ),
        ]
    ),
    RegExLabel(
        label='QUANTITY',
        regexes=[
            RegEx(expressions=[
                r'(?<=\s)-?\d{1,3}(?=\b)',
            ])
        ]
    ),
    RegExLabel(
        label='EVENT',
        regexes=[
            RegEx(
                expressions=[
                    r'\b(?:kicks|punts|pass incomplete|pass|scrambles|rush|sacked)\b',
                ],
                flags=re.IGNORECASE
            )
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
    RegExRelationLabelBuilder('is_spot_of_ball') \
        .add_e1_to_e2(
            e1='TEAM',
            relation_expressions=[
                r'\s+',
            ],
            e2='QUANTITY',
        ) \
        .build()
]
