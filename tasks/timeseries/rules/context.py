from extr.entities.context import ConTextRule, \
                                  ConTextRuleGroup, \
                                  DirectionType


rule_grouping = ConTextRuleGroup(
    rules=[
        ConTextRule(
            'NEGATED',
            ['NEGATIVE_LEFT'],
            direction=DirectionType.LEFT,
            window_size=1
        ),
    ]
)
