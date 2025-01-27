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

## Deploy manually via artifact registery and google cloud run

- **1. Tag an image and push it to artifact registry** (Example)
  The repo name here is `ga-analytics-repo`, the image name `ga_aggs` and the project id `dataops-forge`.

  ```bash
  docker tag ga_aggs europe-west9-docker.pkg.dev/dataops-forge/ga-analytics-repo/ga_aggs
  docker push europe-west9-docker.pkg.dev/dataops-forge/ga-analytics-repo/ga_aggs
  ```

- **2. Deploy the image to cloud run**

  ```bash
  gcloud run deploy ga-aggs-service \
    --image europe-west9-docker.pkg.dev/dataops-forge/ga-analytics-repo/ga_aggs \
    --region europe-west9 \
    --platform managed \
    --allow-unauthenticated \
    --port 8000
  ```

  You should get a response like this :

  ```bash
  The following APIs are not enabled on project [dataops-forge]:
        run.googleapis.com

  Do you want enable these APIs to continue (this will take a few minutes)? (Y/n)?  Y

  Enabling APIs on project [dataops-forge]...
  Operation "operations/acf.p2-253697463975-9130a522-26ad-41f4-b517-fc30339ad7a2" finished successfully.
  Deploying container to Cloud Run service [ga-aggs-service] in project [dataops-forge] region [europe-west9]
  ✓ Deploying new service... Done.
    ✓ Creating Revision...
    ✓ Routing traffic...
    ✓ Setting IAM Policy...
  Done.
  Service [ga-aggs-service] revision [ga-aggs-service-00001-27b] has been deployed and is serving 100 percent of traffic.
  Service URL: https://ga-aggs-service-253697463975.europe-west9.run.app
  ```

  You can test your service by going to the specified **Service URL**, here it is `https://ga-aggs-service-253697463975.europe-west9.run.app`

### Method 1 : Deploy using `gcloud run deploy`

### Method 2 : Deploy using yaml configuration file [TO BE COMPLETED]

- **1. Configure ga-aggs-service.yaml**

  ```yaml
  apiVersion: serving.knative.dev/v1
  kind: Service
  metadata:
    name: ga-aggs-service
    namespace: default
  spec:
    template:
      spec:
        containers:
          - image: europe-west9-docker.pkg.dev/dataops-forge/ga-analytics-repo/ga_aggs
            env:
              - name: GOOGLE_APPLICATION_CREDENTIALS
                value: "/app/secrets/service-account.json"
            ports:
              - containerPort: 8000
            resources:
              limits:
                cpu: "1"
                memory: "512Mi"
  ```

## Deploy manually via cloudbuild & cloud run [Recommended method]

- Place yourself in the right execution context, i.e. @ `DataOps-Forge` root, otherwise the build won't work.

  ```bash
  cd DataOps-Forge
  ```

- Load env variables for this service/public_api:

  ```bash
  source services/public_apis/ga_aggs/.env
  ```

- Trigger the build

  ```bash
  gcloud builds submit --config=services/public_apis/ga_aggs/cloudbuild.yaml .
  ```

  This should build and deploy the app. It will give back a URL which should let you access the deployed app.

  ```plaintext
  ...
  Step #1 - "Push Docker Image to Artifact Registry": bc8b0a883276: Pushed
  Step #1 - "Push Docker Image to Artifact Registry": latest: digest: sha256:89e7639496be334ec29ea8d02f102cbca28ee401a87b1ddb094b56c291045b47 size: 2835
  Finished Step #1 - "Push Docker Image to Artifact Registry"
  Starting Step #2 - "Deploy to Cloud Run"
  Step #2 - "Deploy to Cloud Run": Already have image (with digest): gcr.io/cloud-builders/gcloud
  Step #2 - "Deploy to Cloud Run": Deploying container to Cloud Run service [ga-aggs-service] in project [dataops-forge] region [europe-west9]
  Step #2 - "Deploy to Cloud Run": Deploying...
  Step #2 - "Deploy to Cloud Run": Creating Revision.......................................................................................................................................................................................................................................done
  Step #2 - "Deploy to Cloud Run": Routing traffic.....done
  Step #2 - "Deploy to Cloud Run": Done.
  Step #2 - "Deploy to Cloud Run": Service [ga-aggs-service] revision [ga-aggs-service-00005-2nq] has been deployed and is serving 100 percent of traffic.
  Step #2 - "Deploy to Cloud Run": Service URL: https://ga-aggs-service-253697463975.europe-west9.run.app
  Finished Step #2 - "Deploy to Cloud Run"
  PUSH
  DONE
  ----------------------------------------------------------------------------------------------------------------------------------------------------
  ID                                    CREATE_TIME                DURATION  SOURCE
                      IMAGES  STATUS
  b64d1bbe-c313-4893-89ed-b708052d5ad1  2025-01-05T18:05:12+00:00  2M10S     gs://dataops-forge_cloudbuild/source/1736100311.494846-c647dd55f54b4351a3fdee8c6eb39da2.tgz  -       SUCCESS
  ```

  Here the URL is `https://ga-aggs-service-253697463975.europe-west9.run.app`

  N.B: It won't probably be accessible unless you use the right Bearer token.
  If your GCP user is authorized to perform this operation, then the following command should return a response

  ```bash
  curl -H "Authorization: Bearer $(gcloud auth print-identity-token)"   https://ga-aggs-service-253697463975.europe-west9.run.app
  ```

  Response :

  ```json
  [
    { "total_page_views": 1, "hit_number": 1, "time": 1 },
    { "total_page_views": 3, "hit_number": 3, "time": 3 },
    ...
    { "total_page_views": 1, "hit_number": 1, "time": 1 }
  ]
  ```

- [Optional] Enable public access. Warning : If you get ddos with this, it'll be expensive.

  ```bash
  gcloud run services add-iam-policy-binding ga-aggs-service \
    --region europe-west9 \
    --member="allUsers" \
    --role="roles/run.invoker"
  ```

## Setup autodeploy using github actions to trigger cloud build
