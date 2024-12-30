import os
from google.cloud import bigquery
from engine.data_pipelines.microservices.google_analytics_pipeline import RENAMER_SESSIONS_HITS, QUERY_SESSIONS_HITS
from engine.data_pipelines.common.logging import LOGGER
from engine.data_pipelines.common.data_ops.extract.bigquery import read_from_bigquery
from engine.data_pipelines.common.data_ops.transform.stage_columns import column_selection_and_renaming


def main():
    LOGGER.info("Verify authentication.")

    # Check if GOOGLE_APPLICATION_CREDENTIALS is set
    credentials_path = os.getenv("GOOGLE_APPLICATION_CREDENTIALS")
    if not credentials_path:
        raise EnvironmentError("GOOGLE_APPLICATION_CREDENTIALS is not set.")

    # Initialize BigQuery client
    client = bigquery.Client()

    LOGGER.info("Extract data.")
    df = read_from_bigquery(
        query=QUERY_SESSIONS_HITS,
        project_id="dataops-forge",
        credentials=client._credentials,  # Pass client credentials
    )

    LOGGER.info("Transform - Staging")
    df_renamed = column_selection_and_renaming(df=df, dict_renamers=RENAMER_SESSIONS_HITS)

    LOGGER.info("Transform - Aggregate")
    df_agg = df_renamed.groupby("referer").count()

    LOGGER.info("OUTPUT DATA (in logs)")
    LOGGER.info(df_agg)

    return df_agg
