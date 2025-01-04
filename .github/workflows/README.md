# Creating a Service Account for CI/CD with Required Roles

## Purpose

Set up a service account with the necessary permissions for building, deploying, and managing Docker images using Google Cloud Build, Cloud Run, and Artifact Registry.

---

1. Load environment variables from `.env` file and the service account name

   ```bash
   source .env
   ```

   - **Environment Variables:**
     - `GCP_PROJECT_ID`: The Google Cloud project ID.
     - `BUILD_AND_RELEASE_SERVICE_ACCOUNT_NAME`: The name of the service account.

2. Create the Service Account:

   ```bash
   gcloud iam service-accounts create $BUILD_AND_RELEASE_SERVICE_ACCOUNT_NAME --project $GCP_PROJECT_ID --display-name "Service Account for CI/CD"
   ```

3. Assign Roles to the Service Account:

   - Cloud Build Editor
   - Cloud Run Admin
   - Viewer
   - Logs Writer
   - Secret Manager Secret Accessor
   - Artifact Registry Writer
   - Artifact Registry Reader (Optional)

   ```bash
   #!/bin/bash
   source .env
   SERVICE_ACCOUNT="$BUILD_AND_RELEASE_SERVICE_ACCOUNT_NAME@$GCP_PROJECT_ID.iam.gserviceaccount.com"
   ROLES=(
     "roles/cloudbuild.builds.editor"
     "roles/run.admin"
     "roles/viewer"
     "roles/logging.logWriter"
     "roles/secretmanager.secretAccessor"
     "roles/artifactregistry.writer"
     "roles/artifactregistry.reader"
   )
   for ROLE in "${ROLES[@]}"; do
     gcloud projects add-iam-policy-binding "$GCP_PROJECT_ID" --member="serviceAccount:$SERVICE_ACCOUNT" --role="$ROLE"
   done
   ```

4. Verify the Service Account Roles:

   ```bash
   gcloud projects get-iam-policy $GCP_PROJECT_ID --flatten="bindings[].members" --format="table(bindings.role)" --filter="bindings.members:$BUILD_AND_RELEASE_SERVICE_ACCOUNT_NAME@$GCP_PROJECT_ID.iam.gserviceaccount.com"
   ```

5. Save the Service Account Key (Optional):

   ```bash
   gcloud iam service-accounts keys create key.json --iam-account $BUILD_AND_RELEASE_SERVICE_ACCOUNT_NAME@$GCP_PROJECT_ID.iam.gserviceaccount.com

   ```

6. Save the key in github secrets, then delete the key.json:
   - Name of the secret (Choose service account namen replace `-` with `_`)

## Running cloud build to save artifacts and deploy using google run

- For deploying `ga_aggs` app :

  ```bash
   gcloud builds submit --config=cloudbuild.yaml --substitutions=_SERVICE_NAME=my-service,_REPO_NAME=ga_aggs
  ```

## Clean artifacts & cloud run [Exercice with caution]

1. Load environment variables from relevant `.env` files

   ```bash
   cd <root-of-the-repo>
   source .env  # Project env vars
   source services/public_apis/ga_aggs/.env  # Env vars of app/service to delete
   ```

2. Delete cloud run service

   ```bash
   gcloud run services delete "$SERVICE_NAME" --region "$REGION" --platform managed --quiet
   ```

3. Delete docker images from artifact registry

   ```bash
   gcloud artifacts docker images delete "gcr.io/$PROJECT_ID/$APP_NAME" --delete-tags --quiet
   ```

4. Clean up associated resources (Optional)

   Build history

   ```bash
   gcloud builds list --filter="images:gcr.io/$PROJECT_ID/$APP_NAME" --format="value(id)" | \
   xargs -I {} gcloud builds delete {} --quiet
   ```

   Delete secrets (if any)

   ```bash
   gcloud secrets delete SECRET_NAME
   ```
