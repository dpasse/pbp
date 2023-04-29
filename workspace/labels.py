from typing import Dict, List
import re

from extr.regexes import RegEx, RegExLabel


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
        'Amon-Ra St. Brown',
        'Travis Etienne Jr.',
        'Jeff Wilson Jr.',
        'Velus Jones Jr.',
        'Melvin Gordon III',
        'Tony Fields II',
        'L.Vander Esch',
        'Ray-Ray McCloud III',
        'Joey Slye',
        'PJ Walker',
        'A.J. Brown',

        ### awful.
        'Jack',
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
        'Holder',
        'quarterback'
    ],
    'TEAM': [
        'ARZ',
        'Arizona',
        'ATL',
        'Atlanta',
        'BLT',
        'Baltimore',
        'BUF',
        'Buffalo',
        'CAR',
        'Carolina',
        'CHI',
        'Chicago',
        'CIN',
        'Cinncinatti',
        'CLV',
        'Cleveland',
        'DAL',
        'Dallas',
        'DEN',
        'Denver',
        'DET',
        'Detroit',
        'GB',
        'Green Bay',
        'HST',
        'Houston',
        'IND',
        'Indianapolis',
        'JAX',
        'Jacksonville',
        'KC',
        'Kansas City',
        'LA',
        'Los Angeles Rams',
        'LAC',
        'Los Angeles Chargers',
        'LV',
        'Las Vegas',
        'MIA',
        'Miami',
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
        'Philadelphia',
        'PIT',
        'Pittsburgh',
        'SEA',
        'Seattle',
        'SF',
        'San Francisco',
        'TB',
        'Tampa Bay',
        'TEN',
        'Tennessee',
        'WAS',
        'Washington',
    ]
}

entity_patterns: List[RegExLabel] = [
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
                r'\b[A-Z][\'A-Za-z]+ ([A-Z][a-z]+|-)+(?= (?:[Pp]ass [Ff]rom|PAT |has been ruled out))',
                r'(?<=[Pp]ass [Ff]rom )[A-Z][a-z]+ [A-Z][a-z]+(?= (?:for\b|\())',
                r'\b[A-Z][\'A-Za-z]+ ([A-Z][a-z]+|-)+(?= -?\d+ Yd (?:[Rr]ush|(?:Interception|KO) Return|Run|[Pp]ass [Ff]rom|Field Goal))',
                r'(?<=Injury Update: )[A-Z][\'A-Za-z]+ ([A-Z][a-z]+|-)+?(?= has )'
            ]),
        ]
    ),
    RegExLabel(
        label='FORMATION',
        regexes=[
            RegEx(
                expressions=[
                    r'\b(?:no huddle|shotgun)(?=\b)',
                    r'\b(?:pass|punt|run|field goal|kick) formation(?=\b)'
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
                r'(?<=[\s\(])-?\d{1,3}(?=\b)',
            ])
        ]
    ),
    RegExLabel(
        label='EVENT',
        regexes=[
            RegEx(
                expressions=[
                    r'\b(?:kicks|punts|pass incomplete|pass|scrambles|rush|sack(?:ed)?)\b',
                ],
                flags=re.IGNORECASE
            )
        ]
    )
]
