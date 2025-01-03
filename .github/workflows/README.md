# Creating a Service Account for CI/CD with Required Roles

## Purpose

Set up a service account with the necessary permissions for building, deploying, and managing Docker images using Google Cloud Build, Cloud Run, and Artifact Registry.

---

1. Create the Service Account:

   ```bash
   gcloud iam service-accounts create dataops-forge-sa \
    --display-name "Service Account for CI/CD"
   ```

2. Assign Roles to the Service Account:

   - Cloud Build Editor:
   - Cloud Run Admin:
   - Viewer:
   - Logs Writer:
   - Secret Manager Secret Accessor:
   - Artifact Registry Writer:
   - Artifact Registry Reader (Optional):

     ```bash
     gcloud projects add-iam-policy-binding YOUR_PROJECT_ID \
      --member="serviceAccount:dataops-forge-sa@YOUR_PROJECT_ID.iam.gserviceaccount.com" \
      --role="roles/cloudbuild.builds.editor"

     gcloud projects add-iam-policy-binding YOUR_PROJECT_ID \
      --member="serviceAccount:dataops-forge-sa@YOUR_PROJECT_ID.iam.gserviceaccount.com" \
      --role="roles/run.admin"

     gcloud projects add-iam-policy-binding YOUR_PROJECT_ID \
      --member="serviceAccount:dataops-forge-sa@YOUR_PROJECT_ID.iam.gserviceaccount.com" \
      --role="roles/viewer"

     gcloud projects add-iam-policy-binding YOUR_PROJECT_ID \
      --member="serviceAccount:dataops-forge-sa@YOUR_PROJECT_ID.iam.gserviceaccount.com" \
      --role="roles/logging.logWriter"

     gcloud projects add-iam-policy-binding YOUR_PROJECT_ID \
      --member="serviceAccount:dataops-forge-sa@YOUR_PROJECT_ID.iam.gserviceaccount.com" \
      --role="roles/secretmanager.secretAccessor"

     gcloud projects add-iam-policy-binding YOUR_PROJECT_ID \
      --member="serviceAccount:dataops-forge-sa@YOUR_PROJECT_ID.iam.gserviceaccount.com" \
      --role="roles/artifactregistry.writer"

     gcloud projects add-iam-policy-binding YOUR_PROJECT_ID \
      --member="serviceAccount:dataops-forge-sa@YOUR_PROJECT_ID.iam.gserviceaccount.com" \
      --role="roles/artifactregistry.reader"
     ```

3. Verify the Service Account Roles:

   ```bash
   gcloud projects get-iam-policy YOUR_PROJECT_ID \
    --flatten="bindings[].members" \
    --format="table(bindings.role)" \
    --filter="bindings.members:dataops-forge-sa@YOUR_PROJECT_ID.iam.gserviceaccount.com"
   ```

4. Save the Service Account Key (Optional):

   ```bash
   gcloud iam service-accounts keys create key.json \
    --iam-account dataops-forge-sa@YOUR_PROJECT_ID.iam.gserviceaccount.com
   ```

---

## Notes

- Replace `YOUR_PROJECT_ID` with your actual GCP project ID.
- Keep the `key.json` file secure if it’s used in external CI/CD pipelines.
- To avoid managing keys manually, consider using **Workload Identity Federation**.
