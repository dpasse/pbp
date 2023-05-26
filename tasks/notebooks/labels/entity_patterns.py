import re
from extr import RegEx, \
                 RegExLabel

entity_patterns = [
    RegExLabel(
        label='TIME',
        regexes=[
            RegEx(expressions=[
                r'\b[0-9]{1,2}:[0-9]{2}\b',
            ]),
        ],
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
        label='SCORE',
        regexes=[
            RegEx(
                expressions=[
                    r'(field goal|touchdown)',
                ],
                flags=re.IGNORECASE
            )
        ]
    ),
]

context_patterns = [
    RegExLabel(
        label='NEGATIVE_LEFT',
        regexes=[
            RegEx(expressions=[
                r'\bNULLIFIED by\b',
                r'\bis NO GOOD\b',
            ]),
        ],
    ),
]

patterns = []
patterns.extend(entity_patterns)
patterns.extend(context_patterns)
