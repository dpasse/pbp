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
        label='QUARTER',
        regexes=[
            RegEx(expressions=[
                r'(\d(st|nd|rd|th)|OT)',
            ])
        ]
    ),
    RegExLabel(
        label='EVENT',
        regexes=[
            RegEx(
                expressions=[
                    r'(field goal|extra point)',
                    r'(safety)',
                    r'(touchdown)',
                    r'(penalty)',
                    r'(kicks|punts)',
                    r'(intercepted|fumbles)',
                    r'(sacked)',
                    r'(timeout)'
                ],
                flags=re.IGNORECASE
            ),
            RegEx(
                expressions=[
                    r'(RECOVERED|INTERCEPTED)',
                ],
            )
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
        label='UNITS',
        regexes=[
            RegEx(
                expressions=[
                    r'\b(?:yards?)\b',
                ],
                flags=re.IGNORECASE
            ),
        ]
    ),
    RegExLabel(
        label='PLAYER',
        regexes=[
            RegEx(expressions=[
                r'\b[A-Z][a-z]*\.[A-Z][\'A-Za-z]+\b',
            ])
        ]
    )
]

context_patterns = [
    RegExLabel(
        label='NEGATIVE_LEFT',
        regexes=[
            RegEx(
                expressions=[
                    r'\bNULLIFIED by\b',
                    r'\bis NO GOOD\b',
                ],
                flags=re.IGNORECASE
            ),
        ],
    ),
]

patterns = []
patterns.extend(entity_patterns)
patterns.extend(context_patterns)
