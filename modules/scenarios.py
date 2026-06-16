# modules/scenarios.py

import math
import pandas as pd


def create_what_if_analysis(
    max_teams,
    project_sqft,
    effective_daily_prod,
    travel_days_per_month,
    daily_team_cost
):

    rows = []

    for teams in range(
        1,
        max_teams + 1
    ):

        raw_days = (
            project_sqft /
            (
                effective_daily_prod *
                teams
            )
        )

        travel_days = (
            raw_days / 30
        ) * travel_days_per_month

        total_days = math.ceil(
            raw_days +
            travel_days
        )

        productive_days = (
            total_days -
            travel_days
        )

        utilization = (
            productive_days /
            total_days
        ) * 100

        execution_cost = (
            daily_team_cost *
            total_days *
            teams
        )

        rows.append({
            "Teams": teams,
            "Days Required": total_days,
            "Travel Days":
                round(travel_days, 1),
            "Productive Days":
                round(productive_days, 1),
            "Utilization %":
                round(utilization, 1),
            "Execution Cost":
                round(execution_cost)
        })

    return pd.DataFrame(rows)
