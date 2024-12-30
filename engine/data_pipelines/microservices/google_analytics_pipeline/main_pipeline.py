import os

from google.oauth2.credentials import Credentials

from engine.data_pipelines.microservices.google_analytics_pipeline import RENAMER_SESSIONS_HITS, QUERY_SESSIONS_HITS

from engine.data_pipelines.common.logging import LOGGER
from engine.data_pipelines.common.data_ops.extract.bigquery import read_from_bigquery
from engine.data_pipelines.common.data_ops.transform.stage_columns import column_selection_and_renaming


def main():

    LOGGER.info("Verify authentication.")
    # Get the token from the environment variable
    token = os.getenv("GOOGLE_AUTH_TOKEN")
    if not token:
        raise EnvironmentError("GOOGLE_AUTH_TOKEN is not set.")

    # Use the token to create credentials
    credentials = Credentials(token=token)

    LOGGER.info("Extract data.")
    df = read_from_bigquery(
        query=QUERY_SESSIONS_HITS,
        project_id="dataops-forge",
        credentials=credentials,
    )

    LOGGER.info("Transform - Staging")
    df_renamed = column_selection_and_renaming(df=df, dict_renamers=RENAMER_SESSIONS_HITS)

    LOGGER.info("Transform - Aggregate")
    df_agg = df_renamed.groupby("referer").count()

    LOGGER.info("OUTPUT DATA (in logs)")
    LOGGER.info(df_agg)

    return df_agg
