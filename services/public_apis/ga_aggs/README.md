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

## Locally via cloud run emulator [WIP]

- Run the command

  ```bash
    gcloud beta run services replace /home/iyid/workspaces/DataOps-Forge/services/public_apis/ga_aggs/ga-aggs-service.yaml --dry-run
  ```

- TODO : Options

  - **Option 1: Integrate the service account key within the container image for ease of testing, but never for production..** - [ ] Change the Dockerfile to add `COPY /home/iyid/workspaces/DataOps-Forge/.gcp/dataops-forge-local_container_dev_tester_bq.json /app/secrets/service-account.json
ENV GOOGLE_APPLICATION_CREDENTIALS=/app/secrets/service-account.json` - [ ] Rebuild the image - [ ] Test with the gclodu beta run services ...
  - **Option 2: Use Workload Identity (recommended for production)**

    - [ ] Grant the necessary roles to the service account:

      ```bash
        gcloud projects add-iam-policy-binding <your-project-id> \
        --member="serviceAccount:<your-service-account>@<your-project-id>.iam.gserviceaccount.com" \
        --role="roles/bigquery.dataViewer"
      ```

    - [ ] Deploy the service using Workload Identity:

      ```bash
        gcloud run deploy ga-aggs-service \
        --image gcr.io/<your-project-id>/ga_aggs \
        --region us-central1 \
        --allow-unauthenticated \
        --service-account <your-service-account>@<your-project-id>.iam.gserviceaccount.com
      ```

  - **Option 3: Use Google Cloud Secret Manager**

    - [ ] Upload the service account key to Secret Manager:

      ```bash
        gcloud secrets create service-account-key \
         --data-file=/home/iyid/workspaces/DataOps-Forge/.gcp/dataops-forge-local_container_dev_tester_bq.json
      ```

    - [ ] Grant the service account access to the secret:

    ```bash
       gcloud secrets add-iam-policy-binding service-account-key \
        --member="serviceAccount:<your-service-account>@<your-project-id>.iam.gserviceaccount.com" \
        --role="roles/secretmanager.secretAccessor"
    ```

    - [ ] Deploy the service with Secret Manager access:

      ```bash
        gcloud run deploy ga-aggs-service \
        --image gcr.io/<your-project-id>/ga_aggs \
        --region us-central1 \
        --allow-unauthenticated \
        --service-account <your-service-account>@<your-project-id>.iam.gserviceaccount.com
      ```

    - [ ] Modify the code to fetch the service account key dynamically at runtime

  - **Option 4: Use Google Cloud Storage**

    - [ ] Upload the service account key to a GCS bucket:

      ```bash
        gsutil cp /home/iyid/workspaces/DataOps-Forge/.gcp/dataops-forge-local_container_dev_tester_bq.json gs://<your-bucket-name>/service-account.json
      ```

    - [ ] Grant the service account access to the bucket:

      ```bash
        gsutil iam ch serviceAccount:<your-service-account>@<your-project-id>.iam.gserviceaccount.com:roles/storage.objectViewer gs://<your-bucket-name>
      ```

    - [ ] Modify the application code to download the key at runtime
    - [ ] Deploy the service pointing to the key's location in GCS.
