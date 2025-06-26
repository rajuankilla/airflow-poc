# Apache Airflow Docker Project

A comprehensive Apache Airflow setup running on Docker Desktop with multiple executor configurations and example DAGs demonstrating various Airflow concepts.

## 📋 Table of Contents

- [Prerequisites](#prerequisites)
- [Project Structure](#project-structure)
- [Quick Start](#quick-start)
- [Docker Configurations](#docker-configurations)
- [Virtual Environment Setup (UV)](#virtual-environment-setup-uv)
- [Example DAGs](#example-dags)
- [Accessing Airflow](#accessing-airflow)
- [Useful Commands](#useful-commands)
- [Troubleshooting](#troubleshooting)

## 🔧 Prerequisites

- **Docker Desktop** installed and running
- **Docker Compose** (included with Docker Desktop)
- **UV** (Python package manager) - [Install UV](https://docs.astral.sh/uv/getting-started/installation/)
- At least **4GB RAM** and **2 CPU cores** available for Docker
- **10GB** free disk space

## 📁 Project Structure

```
airflow-docker-project/
├── dags/                           # Airflow DAGs directory
│   ├── branch.py                   # Branching example with @task.branch
│   ├── celery.py                   # Celery executor example
│   ├── group.py                    # Task groups example
│   ├── user.py                     # Asset-based DAGs
│   ├── user_processing.py          # Database operations
│   └── xcom.py                     # XCom data passing
├── logs/                           # Airflow logs
├── plugins/                        # Custom plugins
├── config/                         # Airflow configuration
├── docker-compose.yaml             # Default LocalExecutor setup
├── docker-compose-1-worker-celery.yaml      # Single Celery worker
├── docker-compose-2-worker-nodes-celery.yaml # Two Celery workers
├── docker-compose-without-CeleryExecu.yaml  # LocalExecutor only
├── pyproject.toml                  # UV project configuration
└── README.md                       # This file
```

## 🚀 Quick Start

### 1. Clone and Setup

```bash
git clone https://github.com/rajuankilla/YOUR-PROJECT-NAME.git
cd YOUR-PROJECT-NAME
```

### 2. Set Environment Variables (Linux/Mac)

```bash
echo -e "AIRFLOW_UID=$(id -u)" > .env
```

### 3. Start Airflow (LocalExecutor - Recommended for development)

```bash
docker-compose up -d
```

### 4. Initialize Airflow (First time only)

```bash
docker-compose run --rm airflow-init
```

### 5. Access Airflow Web UI

Open your browser and navigate to: `http://localhost:8080`

**Default credentials:**
- Username: `airflow`
- Password: `airflow`

## 🐳 Docker Configurations

This project includes multiple Docker Compose configurations for different use cases:

### 1. Default Configuration (`docker-compose.yaml`)
- **Executor**: LocalExecutor
- **Database**: PostgreSQL
- **Use case**: Development and small workloads
- **Services**: API Server, Scheduler, DAG Processor, Triggerer

```bash
docker-compose up -d
```

### 2. Single Celery Worker (`docker-compose-1-worker-celery.yaml`)
- **Executor**: CeleryExecutor
- **Database**: PostgreSQL
- **Message Broker**: Redis
- **Workers**: 1 Celery worker
- **Monitoring**: Flower UI available

```bash
docker-compose -f docker-compose-1-worker-celery.yaml up -d
```

Access Flower UI: `http://localhost:5555`

### 3. Multiple Celery Workers (`docker-compose-2-worker-nodes-celery.yaml`)
- **Executor**: CeleryExecutor
- **Workers**: 2 Celery workers for parallel processing
- **Best for**: High-throughput workloads

```bash
docker-compose -f docker-compose-2-worker-nodes-celery.yaml up -d
```

### 4. LocalExecutor Only (`docker-compose-without-CeleryExecu.yaml`)
- Minimal setup without Redis
- Single-node execution

## 🐍 Virtual Environment Setup (UV)

For local development and testing outside Docker:

### 1. Install UV

```bash
# macOS/Linux
curl -LsSf https://astral.sh/uv/install.sh | sh

# Windows
powershell -c "irm https://astral.sh/uv/install.ps1 | iex"
```

### 2. Create Virtual Environment

```bash
# Initialize UV project (if pyproject.toml doesn't exist)
uv init

# Install dependencies
uv add apache-airflow[postgres,celery,redis]
uv add apache-airflow-providers-postgres
uv add apache-airflow-providers-common-sql

# Activate virtual environment
source .venv/bin/activate  # Linux/Mac
# or
.venv\Scripts\activate     # Windows
```

### 3. Local Airflow Setup

```bash
# Set Airflow home
export AIRFLOW_HOME=$(pwd)

# Initialize database
airflow db init

# Create admin user
airflow users create \
    --username admin \
    --firstname Admin \
    --lastname User \
    --role Admin \
    --email admin@example.com \
    --password admin

# Start Airflow locally
airflow webserver --port 8080 &
airflow scheduler
```

## 📊 Example DAGs

### 1. **Branch DAG** (`branch.py`)
Demonstrates the `@task.branch` decorator for conditional workflow execution.

**Key Concepts:**
- Branching logic based on task output
- Conditional task execution
- Task dependency management

```python
@task.branch
def b(val: int):
    if val == 2:
        return "equal_1"
    return "not_equal_one"
```

### 2. **Celery DAG** (`celery.py`)
Shows parallel task execution with Celery workers.

**Features:**
- Parallel task execution
- Worker distribution
- Task dependencies

### 3. **Task Groups** (`group.py`)
Demonstrates organizing tasks into logical groups.

**Benefits:**
- Better DAG visualization
- Nested task groups
- Configurable retry policies per group

### 4. **Asset-based DAGs** (`user.py`)
Modern Airflow 3.0 asset-driven workflows.

**Concepts:**
- Asset scheduling
- Data-driven pipelines
- Multi-outlet assets

### 5. **Database Operations** (`user_processing.py`)
Complete ETL pipeline with PostgreSQL integration.

**Features:**
- API data extraction
- Data transformation
- Database loading
- Sensor-based triggering

### 6. **XCom Usage** (`xcom.py`)
Data passing between tasks using XCom.

**Demonstrates:**
- Task-to-task data transfer
- Return value handling
- Data serialization

## 🌐 Accessing Airflow

### Web UI
- **URL**: `http://localhost:8080`
- **Username**: `airflow`
- **Password**: `airflow`

### Flower (Celery Monitoring)
Available when using Celery configurations:
- **URL**: `http://localhost:5555`

### Database Connection
- **Host**: `localhost`
- **Port**: `5432`
- **Database**: `airflow`
- **Username**: `airflow`
- **Password**: `airflow`

## 💻 Useful Commands

### Docker Operations

```bash
# Start all services
docker-compose up -d

# Stop all services
docker-compose down

# View logs
docker-compose logs -f

# View specific service logs
docker-compose logs -f airflow-scheduler

# Execute commands in Airflow container
docker-compose exec airflow-apiserver bash

# Scale Celery workers (for Celery setups)
docker-compose up -d --scale airflow-worker=3
```

### Airflow CLI Commands

```bash
# List DAGs
docker-compose exec airflow-apiserver airflow dags list

# Test a task
docker-compose exec airflow-apiserver airflow tasks test branch a 2024-01-01

# Trigger a DAG
docker-compose exec airflow-apiserver airflow dags trigger branch

# View task instances
docker-compose exec airflow-apiserver airflow tasks states-for-dag-run branch 2024-01-01
```

### UV Commands

```bash
# Add new dependency
uv add package-name

# Update dependencies
uv lock --upgrade

# Run Python script
uv run python script.py

# Show project info
uv show
```

## 🔧 Troubleshooting

### Common Issues

1. **Permission Errors (Linux/Mac)**
   ```bash
   sudo chown -R $USER:$USER logs/ dags/ plugins/ config/
   ```

2. **Port Already in Use**
   ```bash
   # Check what's using port 8080
   lsof -i :8080
   
   # Change port in docker-compose.yaml
   ports:
     - "8081:8080"  # Change to 8081 or any available port
   ```

3. **Memory Issues**
   ```bash
   # Check Docker resources
   docker system df
   
   # Clean up unused containers/images
   docker system prune -a
   ```

4. **DAG Import Errors**
   ```bash
   # Check DAG syntax
   docker-compose exec airflow-apiserver python /opt/airflow/dags/branch.py
   ```

5. **Database Connection Issues**
   ```bash
   # Reset database
   docker-compose down -v
   docker-compose up -d
   ```

### Performance Tuning

**For Heavy Workloads:**
- Use Celery executor with multiple workers
- Increase Docker resource allocation
- Configure `AIRFLOW__CORE__PARALLELISM` environment variable
- Use external database (not for development)

**Resource Monitoring:**
```bash
# Monitor Docker resources
docker stats

# Check Airflow task performance
docker-compose logs -f airflow-scheduler | grep "Task"
```

### Getting Help

- **Airflow Documentation**: [https://airflow.apache.org/docs/](https://airflow.apache.org/docs/)
- **UV Documentation**: [https://docs.astral.sh/uv/](https://docs.astral.sh/uv/)
- **Docker Compose Reference**: [https://docs.docker.com/compose/](https://docs.docker.com/compose/)

---

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Add your DAGs or improvements
4. Test with different executor configurations
5. Submit a pull request

## 📄 License

This project is open source and available under the [Apache License 2.0](LICENSE).