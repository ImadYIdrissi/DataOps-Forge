# Google analytics pipeline testing & deployment

## Local testing

This microservice `google_analytics_pipeline`, contains a simple example of a micro pipeline that extracts data from bigquery and do

1. Make sure you have followed the [instructions to install dependencies](../../microservices/README.md)
2. Build the Docker image

   ```bash
   docker build -t google-analytics-pipeline -f engine/data_pipelines/microservices/google_analytics_pipeline/Dockerfile .
   ```

3. Test locally

   ```bash
   docker run --env-file .secrets.env google-analytics-pipeline
   ```

## Cloud run deployment
