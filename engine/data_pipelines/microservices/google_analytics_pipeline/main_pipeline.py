from engine.data_pipelines.microservices.google_analytics_pipeline import RENAMER_SESSIONS_HITS, QUERY_SESSIONS_HITS
from engine.data_pipelines.common.data_ops.extract.bigquery import read_from_bigquery
from engine.data_pipelines.common.data_ops.transform.stage_columns import column_selection_and_renaming


if __name__ == "__main__":

    # Extract
    df = read_from_bigquery(
        query=QUERY_SESSIONS_HITS,
        project_id="dataops-forge",
    )

    # Transform - Staging
    df_renamed = column_selection_and_renaming(df=df, dict_renamers=RENAMER_SESSIONS_HITS)

    # Transform - Aggregate
    df_agg = df_renamed.groupby("referer").count()

    print("end")
