import pandas as pd
from google.cloud import bigquery

from engine.data_pipelines.common.logging import LOGGER


def read_from_bigquery(query: str, project_id: str) -> pd.DataFrame:
    try:
        client = bigquery.Client(project=project_id)
        LOGGER.info("Initialized BigQuery client.")

        query_job = client.query(query=query)
        LOGGER.debug(f"Executed query :\n {query}")
        result = query_job.result()
        LOGGER.debug("Received result.")

        df = result.to_dataframe()
        LOGGER.debug(f"Loaded result to dataframe of {df.shape[0]} rows.")
        return df
    except Exception as e:
        LOGGER.error("Failed to fetch from BigQuery.")
        raise e
