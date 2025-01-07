# Global CICD documentation

## Setup : Creating a Service Account for CI/CD with Required Roles

**Purpose**: Set up a service account with the necessary permissions for building, deploying, and managing Docker images using Google Cloud Build, Cloud Run, and Artifact Registry.

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

## Deployment how-tos

### Running cloud build to save artifacts and deploy using google run

- For deploying `ga_aggs` app :

  ```bash
   gcloud builds submit --config=cloudbuild.yaml --substitutions=_SERVICE_NAME=my-service,_REPO_NAME=ga_aggs
  ```

### Clean artifacts & cloud run [Exercice with caution]

1. Load environment variables from relevant `.env` files

   ```bash
   cd DataOps-Forge
   source .env  # Project env vars
   source services/public_apis/ga_aggs/.env  # Env vars of app/service to delete
   ```

2. Delete one or all deployed services

   - Option 1 : List the deployed services & delete the one you want

     ```bash
     gcloud run services list --platform managed --region europe-west9
     ```

     Should return a list of deployed services.

     ```playtext
     SERVICE          REGION        URL                                                        LAST DEPLOYED BY                                    LAST DEPLOYED AT
     ✔  ga-aggs-service  europe-west9  https://ga-aggs-service-253697463975.europe-west9.run.app  253697463975-compute@developer.gserviceaccount.com  2025-01-05T19:38:58.943761Z
     ```

     Delete cloud run service

     ```bash
     export SERVICE_NAME=ga-aggs-service # Replace with the service you wish to delete
     gcloud run services delete "$SERVICE_NAME" --region "$REGION" -o-platfrm managed --quiet
     ```

   - Option 2 : Delete all run services (Bulk method, be careful)

     ```bash
      ALL_SERVICE_NAMES=$(gcloud run services list --platform managed --region europe-west9 --format="value(metadata.name)")

      # Loop through each service and delete it
      for SERVICE_NAME in $ALL_SERVICE_NAMES; do
         gcloud run services delete "$SERVICE_NAME" --platform managed --region europe-west9 --quiet
      done
     ```

3. Delete docker images from GCR repositories

   ```bash
   REPO="gcr.io/$GCP_PROJECT_ID"

   echo "Processing repository: $REPO"

   # List all images in the GCR repository
   IMAGES=$(gcloud container images list --repository="$REPO" --format="value(name)")

   # Loop through each image in the repository
   for IMAGE in $IMAGES; do
      echo "Processing image: $IMAGE"

      # List all tags for
      TAGS=$(gcloud container images list-tags "$IMAGE" --format="value(tags)")

      # Delete each tag associated with the image
      for TAG in $TAGS; do
         echo "Deleting image: $IMAGE:$TAG"
         gcloud container images delete "$IMAGE:$TAG" --quiet --force-delete-tags
      done
   done
   ```

4. Delete the `gcr.io` repository: [DOES NOT WORK]

   ```bash
   gcloud artifacts repositories delete "gcr.io" --location="$REGION" --quiet
   ```

5. Clean up associated resources (Optional)

   List the builds of the last 7days (-P7D) and output just their ID. Put this in a var and loop to delete these builds.

   ```bash
   BUILD_IDS=$(gcloud builds list --filter="createTime >= -P7D AND (status=QUEUED OR status=WORKING)" --format="value(ID)")
   for BUILD_ID in $BUILD_IDS; do
      echo "Cancelling build: $BUILD_ID"
      gcloud builds cancel "$BUILD_ID" --quiet
   done
   ```

   If you added permissions (e.g., allUsers for public access), ensure they're cleaned up to avoid unintended access.
   Revoke permissions for allUsers:

   ```bash
   gcloud run services remove-iam-policy-binding ga-aggs-service \
   --region=europe-west9 \
   --member="allUsers" \
   --role="roles/run.invoker"
   ```

   Check and clean up additional IAM bindings if needed:

   ```bash
   gcloud projects get-iam-policy $GCP_PROJECT_ID
   ```

   Delete secrets (if any)

   ```bash
   gcloud secrets delete SECRET_NAME
   ```

6. Verify billing
