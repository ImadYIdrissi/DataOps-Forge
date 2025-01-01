"""Bigquery extract operations."""

import pandas as pd
from google.cloud import bigquery

from engine.data_pipelines.common.logging import LOGGER


def read_from_bigquery(query: str, project_id: str, credentials: str) -> pd.DataFrame:
    """Read data from Google BigQuery and returns it as a Pandas DataFrame.

    Args:
        query (str): The SQL query to execute in BigQuery.
        project_id (str): The Google Cloud project ID under which the query will run and be billed.
        credentials (str): Path to the credentials file or credentials object required for authentication.

    Returns:
        pd.DataFrame: The query result loaded into a Pandas DataFrame.

    Raises:
        Exception: If the query execution or data fetching fails.
    """
    try:
        client = bigquery.Client(project=project_id, credentials=credentials)
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
