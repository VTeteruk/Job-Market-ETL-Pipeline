# Job Market ETL Pipeline

A comprehensive ETL (Extract, Transform, Load) data pipeline built with Apache Airflow, Apache Spark, and PostgreSQL to collect, clean, transform, and analyze job listings for Data Engineer positions from job platforms.

## 🏗️ Architecture

![V1.drawio.png](README_files/V1.drawio.png)

This project implements a modern data engineering architecture using:

- **Apache Airflow** - Workflow orchestration and scheduling
- **Apache Spark** - Distributed data processing
- **PostgreSQL** - Data warehouse with multi-layer architecture
- **Docker** - Containerization for consistent deployment
- **Python** - Data scraping and processing logic

### Data Flow
1. **Scrapers** collect job data from multiple sources (Indeed, LinkedIn, Profesia.sk)
2. **Sources** store raw data as CSV files
3. **Bronze Layer** ingests raw data with full load strategy
4. **Silver Layer** processes and cleans data using Apache Spark
5. **Gold Layer** creates business-ready views and aggregations
6. **Consume** layer provides data for BI & Reporting tools

## 📋 Project Roadmap
Track the development progress and upcoming features on my Notion board:

**📖 [Job Market ETL Pipeline - Project stages](https://www.notion.so/Job-Market-ETL-Pipeline-20f9f8d6df318087b1f0e5df17d56726)**

## 📊 Data Architecture

The pipeline follows a **medallion architecture** with three layers:

### 🥉 Bronze Layer (Raw Data)
- Stores raw, unprocessed job listings scraped from job platforms
- Maintains data lineage and audit trail
- Schema: `bronze.jobs`

### 🥈 Silver Layer (Cleaned Data)
- Contains cleaned, validated, and normalized data
- Salary information parsed into structured format (amount, currency, period)
- Schema: `silver.jobs`

### 🥇 Gold Layer (Analytics-Ready)
- Business-ready views and aggregations
- Views: `gold.most_hiring_location_view`, `gold.market_overview`

## 🚀 Features

- **Automated Web Scraping**: Collects job data from multiple platforms (Currently only from Profesia.sk)
- **Multi-Source Integration**: Designed to handle data from various job platforms
- **Data Quality**: Comprehensive data cleaning and validation
- **Scalable Processing**: Spark-based ETL for handling large datasets
- **Monitoring**: Airflow UI for pipeline monitoring and debugging
- **Database Management**: PgAdmin for database administration
- **Containerized**: Full Docker setup for easy deployment

## 🛠️ Prerequisites

- Docker and Docker Compose
- Python 3.8+
- At least 4GB RAM for Spark processing

## 🚀 Quick Start

### 1. Clone the Repository
```bash
git clone https://github.com/VTeteruk/Job-Market-ETL-Pipeline.git
```

### 2. Start the Services
```bash
docker-compose build
docker-compose up -d
```

### 3. Access the Applications

| Service | URL | Credentials |
|---------|-----|-------------|
| Airflow Web UI | http://localhost:8080 | admin/admin |
| Spark Master UI | http://localhost:8081 | - |
| PgAdmin | http://localhost:5050 | admin@admin.com/admin |

### 4. Initialize the Database Connection in PgAdmin

1. Open PgAdmin at http://localhost:5050
2. Add server with these settings:
   - Host: `postgres`
   - Port: `5432`
   - Database: `job_market_db`
   - Username: `airflow`
   - Password: `airflow`

### 5. Run the Pipeline

1. Open Airflow UI at http://localhost:8080
2. Enable the `run_profesia_sk` DAG
3. Trigger the DAG manually or wait for scheduled execution

## 🔧 Configuration

### Environment Variables
Key configurations in `docker-compose.yml`:

```yaml
AIRFLOW__CORE__SQL_ALCHEMY_CONN: postgresql+psycopg2://airflow:airflow@postgres/job_market_db
AIRFLOW__CORE__EXECUTOR: LocalExecutor
AIRFLOW_CONN_LOCAL_POSTGRES: postgresql://airflow:airflow@postgres:5432/job_market_db
AIRFLOW_CONN_SPARK_DEFAULT: spark://spark-master:7077
```

### Scraping Configuration
Configure scraping parameters in `scrapers/profesiaSK/settings.py`:

```python
BASE_SEARCH_URL = "https://www.profesia.sk/praca/?search_anywhere=data+engineer&sort_by=relevance&page_num={}"
```

## 🔍 Monitoring and Debugging

### Airflow Logs
- Access logs through the Airflow UI
- Logs are stored in `./logs/` directory

### Spark UI
- Monitor Spark jobs at http://localhost:8081
- View job execution details and performance metrics

### Database Monitoring
- Use PgAdmin for database administration
- Monitor query performance and data quality

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

**Built with ❤️ - sharing my data engineering journey**