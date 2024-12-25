from pathlib import Path

from engine.data_pipelines.common.data_ops.extract.bigquery import read_from_bigquery
from engine.data_pipelines.common.data_ops.transform.stage_columns import column_renaming

QUERY_HITS_PER_VISITOR = Path(
    "engine/data_pipelines/microservices/google_analytics_pipeline/sql/hits_sessions_20160801.sql"
)


HITS_SESSIONS_RENAMERS_PATH = Path(
    "engine/data_pipelines/microservices/google_analytics_pipeline/renamers/hits_sessions_20160801.json"
)


if __name__ == "__main__":

    # Extract
    with open(QUERY_HITS_PER_VISITOR) as f:
        query = f.read()
        df = read_from_bigquery(
            query=query,
            project_id="dataops-forge",
        )

    # Transform - Staging
    df_renamed = column_renaming(df=df, json_renamers_path=HITS_SESSIONS_RENAMERS_PATH)

    # Transform - Aggregate
    df_agg = df_renamed.groupby("referer").count()

    print("end")
