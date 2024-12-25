# DataOps-Forge

Repository for managing ETL/ELT pipelines and related infrastructure.

## Repository structure

```plaintext
DataOps-Forge
├── services/
│   └── public_apis/               # API code for exposing data
├── engine/
│   └── data_pipelines/            # Data related code
│       ├── orchestrators/         # Workflow management tools like Airflow or Dagster
│       │   ├── airflow/           # Airflow-specific DAGs and configurations
│       │   └── dagster/           # Dagster-specific pipeline definitions
│       ├── microservices/         # Cloud Run-specific lightweight operations
│       ├── transformations/       # Data transformation logic
│       │   ├── distributed/spark/ # Functions and reusable code for distributed environments
│       │   ├── batch/polars/      # Functions and reusable code for monolithic environments, using Pandas or parallelized with Polars
│       │   └── dbt/               # DBT project files for SQL-based transformations
│       ├── streaming/             # Real-time data processing
│       │   ├── pubsub/            # Google Cloud Pub/Sub producers and consumers
│       │   ├── kafka/             # Kafka-based producers and consumers
│       │   └── flink/             # (Optional) Stateful processing with Apache Flink
│       ├── extraction/            # Scripts for extracting data from various sources
│       ├── loading/               # Scripts for loading data into destinations
│       └── common/                # Shared utilities, configurations, and libraries
├── tests/                         # Unit and integration tests
├── ci_cd/                         # Automation scripts for CI/CD pipelines
├── infra/                         # Terraform scripts and infrastructure as code
└── README.md                      # Documentation for the repository
```
