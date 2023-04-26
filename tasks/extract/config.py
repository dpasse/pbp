from typing import List

from extr.regexes import SlimRegEx, RegEx, RegExLabel
from extr.relations import RegExRelationLabelBuilder


kb = {
    'TEAM': [
        'Kansas City',
        'Cleveland',
        'New Orleans',
    ],
    'PLAYER': [
        r'[AE]\.St\. Brown',
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
        'QB'
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
        'NYJ',
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
        label='DISTANCE',
        regexes=[
            RegEx(expressions=[
                r'(?<=\s)-?\d+\s+(yards?|Yds?)(?=\b)'
            ]),
        ]
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
