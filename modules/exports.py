# modules/exports.py

from io import BytesIO
import pandas as pd


def create_excel_export(
    inputs_df,
    team_df,
    material_df,
    what_if_df,
    scenario_df,
    schedule_df,
    summary_df
):

    output = BytesIO()

    with pd.ExcelWriter(
        output,
        engine="xlsxwriter"
    ) as writer:

        inputs_df.to_excel(
            writer,
            sheet_name="Inputs",
            index=False
        )

        team_df.to_excel(
            writer,
            sheet_name="Team Details",
            index=False
        )

        material_df.to_excel(
            writer,
            sheet_name="Material Costing",
            index=False
        )

        what_if_df.to_excel(
            writer,
            sheet_name="What If Analysis",
            index=False
        )

        schedule_df.to_excel(
            writer,
            sheet_name="Project Schedule",
            index=False
        )

        summary_df.to_excel(
            writer,
            sheet_name="Summary",
            index=False
        )

        scenario_df.to_excel(
            writer,
            sheet_name="Scenario Comparison",
            index=False
        )

    return output.getvalue()
