from pathlib import Path

import pandas as pd
from google.cloud import bigquery

from engine.data_pipelines.common.logging import LOGGER

QUERY_HITS_PER_VISITOR = Path("engine/data_pipelines/extraction/sql/hits_per_visitor_sessions_20160801.sql")


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


if __name__ == "__main__":

    with open(QUERY_HITS_PER_VISITOR) as f:
        query = f.read()
        read_from_bigquery(
            query=query,
            project_id="dataops-forge",
        )

    print("End")
