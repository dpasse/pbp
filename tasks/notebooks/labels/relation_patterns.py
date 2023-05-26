from extr import RegExRelationLabelBuilder

relation_patterns = [
    RegExRelationLabelBuilder('is_at') \
        .add_e2_to_e1(
            e2='TIME',
            relation_expressions=[
                r'(\s+-\s+)',
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
