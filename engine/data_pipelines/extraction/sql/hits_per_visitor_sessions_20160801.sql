WITH src_ga_sessions AS (
    SELECT
        totals,
        hits
    FROM
        `bigquery-public-data.google_analytics_sample.ga_sessions_20160801`
),
stg_hits_per_visitor AS (
    SELECT
        totals.pageViews as total_page_views,
        hits.*
    FROM
        src_ga_sessions,
        UNNEST(src_ga_sessions.hits) AS hits
)
SELECT
    *
FROM
    stg_hits_per_visitor