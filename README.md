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
┃ ┃ ┣ microservices/               # Micro Data pipelines as back-end microservices, not to confuse with DataOps-Forge/services
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

## External dependencies

- Docker / Docker-desktop
- act : To test CICD jobs

## Setup the environment

1. Create virtual env via pyenv, for convention call it dataops-forge
2. Activate virtual env

   ```bash
   pyenv activate dataops-forge
   pip install -U pip pip-tools
   ```

   NB: It is recommended to set up this environment as your default IDE interpreter. 3. Install and update python tools

3. [Optional] if need to update python requirements, then recompile them this way :

   ```bash
   pip-compile requirements.in
   pip-compile requirements.ci.in
   ```

## Run CI locally

Move to the root of the project.

```bash
cd DataOps-Forge
```

We use `act` to test CICD locally, it needs docker to create containers that will be the ci runners.

Test all the CI :

```bash
act
```

Or if you want to test just a particular area

```bash
act -j quality
```

You can also visualize the dependency graph with

```bash
act --graph
```

Example output

```plaintext
INFO[0000] Using docker host 'unix:///var/run/docker.sock', and daemon socket 'unix:///var/run/docker.sock'
             ╭───────────────────────────╮
             │ Get Environment Variables │
             ╰───────────────────────────╯
                           ⬇
       ╭───────────────────────────────────────╮
       │ Setup Python and Install Dependencies │
       ╰───────────────────────────────────────╯
                           ⬇
 ╭────────────────╮ ╭────────────────╮ ╭──────────────╮
 │ Flake8 linting │ │ Security Check │ │ Code Quality │
 ╰────────────────╯ ╰────────────────╯ ╰──────────────╯
```
