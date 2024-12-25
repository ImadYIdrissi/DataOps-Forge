# DataOps-Forge

Repository for managing ETL/ELT pipelines and related infrastructure.

## Repository structure

```plaintext
DataOps-Forge/                     # Root of the repository containing all project components.
┣ .vscode/                         # Configuration for Visual Studio Code settings and debugging.
┣ ci_cd/                           # Directory for CI/CD configuration and automation scripts.
┣ engine/                          # Core directory for all pipeline logic and reusable components.
┃ ┣ data_pipelines/                # Contains modules and logic related to data pipelines.
┃ ┃ ┣ common/                      # Shared utilities and helper modules.
┃ ┃ ┃ ┣ auth/                      # Authentication-related utilities.
┃ ┃ ┃ ┣ data_ops/                  # Generic utilities for data extraction, transformation, and loading.
┃ ┃ ┃ ┣ logging/                   # Centralized logging utilities for consistent logging across all code.
┃ ┃ ┣ microservices/               # Microservices for handling specific business logic or data pipelines.
┃ ┃ ┃ ┣ google_analytics_pipeline/ # Microservice for processing Google Analytics data project.
┃ ┃ ┣ orchestrators/               # Workflow orchestration tools like Airflow or Dagster.
┃ ┃ ┃ ┣ airflow/                   # Placeholder for Airflow-specific configurations and DAGs.
┃ ┃ ┃ ┗ dagster/                   # Placeholder for Dagster-specific pipeline definitions.
┃ ┃ ┣ streaming/                   # Real-time data processing logic and configurations.
┃ ┃ ┃ ┣ flink/                     # Placeholder for Flink-based streaming operations.
┃ ┃ ┃ ┣ kafka/                     # Placeholder for Kafka-based streaming operations.
┃ ┃ ┃ ┗ pubsub/                    # Placeholder for Google Pub/Sub-based streaming operations.
┣ infra/                           # Infrastructure as code (IaC) scripts for provisioning resources.
┣ services/                        # Contains API code for exposing or integrating data.
┃ ┗ public_apis/                   # Placeholder for public-facing APIs.
┗ tests/                           # Contains all test modules for the project.
  ┣ e2e/                           # End-to-end tests for validating full pipeline functionality.
  ┣ integration/                   # Integration tests to validate interactions between modules or services.
  ┗ unit/                          # Unit tests for individual functions or modules.
```
