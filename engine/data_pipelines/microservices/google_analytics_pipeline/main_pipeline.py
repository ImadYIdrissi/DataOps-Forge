import os
from google.cloud import bigquery
from google.auth import default
from engine.data_pipelines.microservices.google_analytics_pipeline import RENAMER_SESSIONS_HITS, QUERY_SESSIONS_HITS
from engine.data_pipelines.common.logging import LOGGER
from engine.data_pipelines.common.data_ops.extract.bigquery import read_from_bigquery
from engine.data_pipelines.common.data_ops.transform.stage_columns import column_selection_and_renaming


def main():
    LOGGER.info("Verify authentication.")

    # Attempt to detect credentials automatically
    try:
        credentials, project = default()
        LOGGER.info("Default credentials detected.")
    except Exception as e:
        # Fallback to GOOGLE_APPLICATION_CREDENTIALS if available
        credentials_path = os.getenv("GOOGLE_APPLICATION_CREDENTIALS")
        if not credentials_path:
            raise EnvironmentError(
                "No valid credentials found. Ensure GOOGLE_APPLICATION_CREDENTIALS is set locally or "
                "Cloud Run has the correct permissions."
            ) from e
        LOGGER.info("Using GOOGLE_APPLICATION_CREDENTIALS for authentication.")
        credentials = None  # Automatically handled by the environment

    # Initialize BigQuery client
    client = bigquery.Client(credentials=credentials, project=project)

    LOGGER.info("Extract data.")
    df = read_from_bigquery(
        query=QUERY_SESSIONS_HITS,
        project_id=project,
        credentials=client._credentials,  # Pass client credentials
    )

    LOGGER.info("Transform - Staging")
    df_renamed = column_selection_and_renaming(df=df, dict_renamers=RENAMER_SESSIONS_HITS)

    LOGGER.info("Transform - Aggregate")
    df_agg = df_renamed.groupby("referer").count()

    LOGGER.info("OUTPUT DATA (in logs)")
    LOGGER.info(df_agg)

    return df_agg
