# Setup

## The Steps to Set Up Google Cloud Run & Artifact Registry for the First Time

To use **Google Cloud Run** and **Google Artifact Registry** for saving images and running containers, follow these steps to set up your billing account and project properly.

---

### **1. Set the Right Project ID**

Ensure that your `gcloud` CLI is set to use the correct project:

```bash
gcloud config set project dataops-forge
```

Verify the active project:

```bash
gcloud config list project
```

---

### **2. Verify API Enablement**

Confirm that the required APIs are enabled for your project.

- Check if the **Artifact Registry API** is enabled:

  ```bash
  gcloud services list --enabled | grep artifactregistry
  ```

- If it’s not enabled, activate it:

  ```bash
  gcloud services enable artifactregistry.googleapis.com
  ```

- Do the same for **Cloud Run API**:

  ```bash
  gcloud services enable run.googleapis.com
  ```

---

### **3. Synchronize Billing**

Ensure that the project is linked to a billing account.

- Verify the billing account:

  ```bash
  gcloud billing projects describe dataops-forge
  ```

- If no billing account is linked, link it:

  ```bash
  gcloud billing projects link dataops-forge --billing-account=<BILLING_ACCOUNT_ID>
  ```

- Replace `<BILLING_ACCOUNT_ID>` with the ID of your billing account. You can find this by listing your billing accounts:

  ```bash
  gcloud billing accounts list
  ```

---

### **4. Update `gcloud` Components**

Ensure your `gcloud` CLI is up to date to avoid issues with new features:

```bash
gcloud components update
```

---

### **5. Create an Artifact Registry Repository**

Set up a Docker repository in Artifact Registry to store your container images.

- Create the repository `ga-analytics-repo`:

  ```bash
  gcloud artifacts repositories create ga-analytics-repo --repository-format=docker --location=europe-west9 --description="Repository for GA Analytics service, with exposed analysis"
  ```

- Verify the repository is created:

  ```bash
  gcloud artifacts repositories list
  ```

## The Steps to Set Up Google Cloud build

### **1.Grant Roles to the Compute Engine Service Account**

If you try to run a gcloud builds command without enabling this you will envounter an error :

<!-- markdownlint-disable MD033 -->
<details>
  <summary>Erroneous command run due to bad permissions</summary>

    - Command example :

      ```bash
      iyid@Torque-007:~/workspaces/DataOps-Forge/services/public_apis/ga_aggs$ gcloud builds submit --config=cloudbuild.yaml --substitutions=_APP_NAME=$APP_NAME,_SERVICE_NAME=$SERVICE_NAME
      ```
    - Output :

      ```plaintext
      Creating temporary archive of 8 file(s) totalling 4.3 KiB before compression.
      Uploading tarball of [.] to [gs://dataops-forge_cloudbuild/source/1735947057.832211-187158dc842c47a1aea19b26432b7346.tgz]
      API [cloudbuild.googleapis.com] not enabled on project [dataops-forge]. Would you like to enable and retry (this will take a few minutes)? (y/N)?  y
      Enabling service [cloudbuild.googleapis.com] on project [dataops-forge]...
      Operation "operations/acf.p2-253697463975-9a8a832d-6aff-4d95-a3f3-2667883b22e8" finished successfully.
      ERROR: (gcloud.builds.submit) FAILED_PRECONDITION: invalid bucket "253697463975.cloudbuild-logs.googleusercontent.com"; service account 253697463975-compute@developer.gserviceaccount.com does not have access to the bucket
      ```

</details>

Run the following commands to fix it

```bash
PROJECT_ID="dataops-forge"
SERVICE_ACCOUNT="253697463975-compute@developer.gserviceaccount.com"
BUCKET_NAME="253697463975.cloudbuild-logs.googleusercontent.com"

# Grant the necessary roles
gcloud storage buckets add-iam-policy-binding gs://$BUCKET_NAME \
    --member=serviceAccount:$SERVICE_ACCOUNT \
    --role=roles/storage.objectCreator

gcloud storage buckets add-iam-policy-binding gs://$BUCKET_NAME \
    --member=serviceAccount:$SERVICE_ACCOUNT \
    --role=roles/storage.objectViewer

```

### Configure artifact registry domain associated with the repo's location

Run the following command to configure gcloud as the credential helper for the Artifact Registry domain associated with this repository's location:

```bash
gcloud auth configure-docker europe-west9-docker.pkg.dev
```
