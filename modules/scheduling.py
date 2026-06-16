# modules/scheduling.py

import pandas as pd
from datetime import timedelta


def create_schedule(
    start_date,
    project_days,
    travel_days
):

    mobilization = 1

    execution_days = (
        project_days -
        int(travel_days)
    )

    completion = 1

    schedule = pd.DataFrame({

        "Phase": [

            "Mobilization",
            "Execution",
            "Travel / Relocation",
            "Completion"

        ],

        "Days": [

            mobilization,
            execution_days,
            round(travel_days, 1),
            completion

        ]

    })

    return schedule
