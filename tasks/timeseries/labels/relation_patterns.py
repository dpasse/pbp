from extr import RegExRelationLabelBuilder

relation_patterns = [
    RegExRelationLabelBuilder('is_at') \
        .add_e2_to_e1(
            e2='TIME',
            relation_expressions=[
                r'(\s+-\s+)',
            ],
            e1='QUARTER'
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
        .build(),
    RegExRelationLabelBuilder('is_unit') \
        .add_e1_to_e2(
            e1='QUANTITY',
            relation_expressions=[
                r'\s+',
            ],
            e2='UNITS',
        ) \
        .build(),
    RegExRelationLabelBuilder('is_on') \
        .add_e1_to_e2(
            e1='EVENT',
            relation_expressions=[
                r'\s+(?:on|by)\s+',
                r'\s+(#\d)\s+by\s+'
            ],
            e2='TEAM',
        ) \
        .build(),
    RegExRelationLabelBuilder('is_on') \
        .add_e1_to_e2(
            e1='EVENT',
            relation_expressions=[
                r'\s+(?:by)\s+',
            ],
            e2='PLAYER',
        ) \
        .build()
]
