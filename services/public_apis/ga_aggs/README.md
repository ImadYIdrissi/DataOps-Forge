# How-to build and run

## Common steps

- Generate & download a key file from GCP's IAM console, and put it in the root of the project `.gcp/dataops-forge-local_container_dev_tester_bq.json`
  - Needed permissions : BigQuery Data Viewer, BigQuery Job User, BigQuery Read Session User

## Locally via docker

- Build the image `docker build -t ga_aggs -f services/public_apis/ga_aggs/Dockerfile .`
- Run the image

  ```bash
    docker run -p 8000:8000 -v ~/workspaces/DataOps-Forge/.gcp/dataops-forge-local_container_dev_tester_bq.json:/app/secrets/service-account.json -e GOOGLE_APPLICATION_CREDENTIALS=/app/secrets/service-account.json ga_aggs
  ```

- Visit `localhost:8000`
