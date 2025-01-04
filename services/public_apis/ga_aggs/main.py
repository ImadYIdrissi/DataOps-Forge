"""Entry point of ga_aggs service."""

import os
import uvicorn
from fastapi import FastAPI

from engine.data_pipelines.microservices.google_analytics_pipeline.main_pipeline import main

app = FastAPI()


@app.get("/")
def get_agg_data():
    """Fetch aggregated data from the Google Analytics pipeline.

    Returns:
        list: A list of dictionaries representing aggregated data in JSON-compatible format.
    """
    # Example DataFrame
    df_agg = main()

    # Convert DataFrame to a JSON-compatible dictionary
    result = df_agg.to_dict(orient="records")

    return result  # Return as a JSON object


if __name__ == "__main__":
    # Serve the FastAPI app on the port provided by the environment variable
    port = int(os.getenv("PORT", "8080"))
    uvicorn.run(app, host="0.0.0.0", port=port)  # nosec
