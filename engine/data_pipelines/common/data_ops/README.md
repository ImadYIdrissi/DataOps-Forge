# Data Ops

The `data_ops` folder provides a collection of utility and helper functions designed to support data pipelines. These utilities are **generic** and **non-business-specific**, making them reusable across various pipelines and microservices.

This folder serves as a central module for common operations related to **data extraction**, **loading**, and **transformation**.

## Folder Structure

- **`extract/`**:
  Contains technology-specific utilities for data extraction, such as reading from tables, files, or storage buckets.

  Example Use Cases:

  - Reading a table from BigQuery.
  - Downloading files from Cloud Storage.
  - Extracting data from APIs.

- **`load/`**:
  Contains technology-specific utilities for data loading, focusing on writing data to tables, files, or storage destinations.

  Example Use Cases:

  - Writing data to a BigQuery table.
  - Uploading files to Cloud Storage.
  - Streaming data into Kafka.

- **`transform/`**:
  Contains logic-specific and generalized transformation operations that can be applied across pipelines.

  Example Use Cases:

  - Renaming or staging columns in dataframes.
  - Decompressing files and parsing raw data.
  - Converting timestamps or parsing dates.

---

## Contributing

To add a new utility:

1. Identify the appropriate subfolder (`extract`, `load`, `transform`).
2. Ensure the function is generic and does not include business-specific logic.
3. Add documentation and unit tests for the new function.
