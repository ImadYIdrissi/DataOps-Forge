# Local Execution of Cloud Run Container with Emulator

## 1. Install Prerequisites

    - Ensure **Docker** is installed and running.
    - Confirm that you have **Google Cloud SDK** installed for authentication and `gcloud` commands.

## 2. Authenticate with Google Cloud

- Authenticate to Gcloud sdk for the first time
  
  ```bash
  gcloud init
  ```

- Set up the default-credentials & place them in the .screts.env file at the root of `DataOps-Forge`

  ```bash
  gcloud auth application-default print-access-token
  ```

- Run the following command to authenticate Docker with Google Cloud:

  ```bash
  gcloud auth configure-docker
  ```

This configures Docker to use Google Cloud credentials, allowing your container to access GCP services like BigQuery.

## 3. Build and Test Your Container

- Build the Docker Image
- Navigate to the directory containing your Dockerfile and build the image:

  ```bash
  docker build -t column-renaming-pipeline .
  ```

- Run the Container Locally
- Use Docker to simulate the execution of your container:

  ```bash
  docker run -it column-renaming-pipeline
  ```

  This will execute your `main.py` script inside the container.

## 4. Use gcloud for Cloud Run Emulator

Although cloud-run-local isn’t available, you can test your container locally using the standard gcloud run commands:

```bash
gcloud run deploy column-renaming-pipeline \
--image column-renaming-pipeline \
--platform managed \
--region us-central1 \
--no-traffic \
--allow-unauthenticated \
--dry-tun
```

Add the --dry-run flag to simulate the deployment without pushing to GCP.

## 5. Debugging

If your container doesn't behave as expected, check its logs:

```bash
docker logs [CONTAINER_ID]
```
