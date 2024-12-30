# How-to build and run

## Common steps

- Generate your gcloud token and place it in `.secrets.env`

  ```bash
  echo "GOOGLE_AUTH_TOKEN=$(gcloud auth application-default print-access-token)" > .secrets.env
  ```

  Make sure the token is correctly set.
  P.S This may need to be ran everytime because the token expires every 60 minutes.

## Locally via docker

- Build the image `docker build -t ga_aggs -f services/public_apis/ga_aggs/Dockerfile .`
- Run the image `docker run -p 8000:8000 --env-file .secrets.env ga_aggs`
- Visit `localhost:8000`