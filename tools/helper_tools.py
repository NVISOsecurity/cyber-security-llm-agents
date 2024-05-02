from typing_extensions import Annotated

def match_techniques_to_caldera_abilities(
    report_techniques: Annotated[
        list,
        "The mitre technique ids extracted from a report",
    ],
    caldera_abilities: Annotated[
        list,
        "The Caldera abilities from the API",
    ]
) -> Annotated[str, "The macthed techniques"]:

    matched_techniques = []

    for report_technique in report_techniques:
        for caldera_ability in caldera_abilities:
            if report_technique == caldera_ability["technique_id"]:
                matched_techniques.append(caldera_ability)

    return matched_techniques
