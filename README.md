# Job Aggregator Platform

A scalable, data-driven Job Aggregator platform that collects, processes, and normalizes job listings from multiple sources (Naukri, Instahyre, Company career pages, and user-submitted links). The platform leverages a decoupled Medallion Architecture via PySpark to clean data and provides real-time dashboard analytics on market trends, tech stack demands, and geographic hiring opportunities.

---

## 🚀 Architecture Overview

To ensure high performance and prevent database starvation on the production instance, the platform completely decouples the data ingestion and transformation layers from the application database.

```
[ Ingestion Layer ]        [ Storage & Processing ]       [ Production Layer ]
 ├── Scrapers (Cron)  ───>  AWS S3 (Bronze Bucket)         
 └── User Links              │                             
                             ▼                             
                        PySpark (Silver ETL)               
                             │                             
                             ▼                             
                        PostgreSQL  <───────────────────>  FastAPI Backend
                     (Production Data)                     (Dashboard Analytics)

```

1. **Ingestion (Bronze):** Cron jobs and user-submitted tracking links fetch raw HTML/JSON data and dump them directly into an object storage landing zone (**AWS S3 / MinIO**).
2. **Processing (Silver):** A **PySpark** pipeline processes the raw data off-cluster, running deduplication, text parsing, and extracting normalized entities (skills, standardized locations, experience ranges, and salaries).
3. **Serving (Gold/Production):** The cleaned records are upserted into **PostgreSQL** to serve high-performance analytical queries to the **FastAPI** backend.

---

## 🗄️ Database Schema Design

The production database is optimized for analytical aggregation and dashboard rendering, avoiding heavy text-processing bottlenecks.

![DB Schema](./docs/db_schema.png)

### Core Production Tables

#### 1. `users`

Tracks authenticated platform users (job seekers or recruiters).

* `id` (PK, integer)
* `username` / `email` / `password` / `role` (varchar)
* `is_active` (boolean)

#### 2. `company_sources`

Stores targets for the web scrapers. Tracks custom career pages or portal tracks.

* `id` (PK, integer)
* `name` (varchar) - e.g., "Tata 1mg"
* `url` (text) - Base URL to scrape.
* `type` (varchar) - e.g., `career_page`, `naukri`, `wellfound`.
* `added_by_user_id` (FK -> `users.id`, Nullable) - Links back if a user requested tracking.

#### 3. `jobs`

The single source of truth for all aggregated, deduplicated, and fully parsed job listings.

* `id` (PK, integer)
* `user_id` (FK -> `users.id`, Nullable) - Set if manually posted by a user.
* `job_title_cleaned` (varchar) - e.g., "Backend Engineer"
* `company_name` / `source_platform` (varchar)
* `source_url` (text, **UNIQUE**) - Prevents duplicate ingestion via upstream upserts.
* `job_description` (text)
* `city_normalized` / `country_normalized` (varchar) - For reliable dashboard filtering.
* `min_experience_years` / `max_experience_years` (integer)
* `salary_min` / `salary_max` (numeric) / `currency` (varchar)
* `posted_at` (timestamp)

#### 4. `skills`

Master catalog of distinct technical skills and keywords.

* `id` (PK, integer)
* `title` (varchar, **UNIQUE**) - e.g., "FastAPI", "Python", "PySpark"
* `category` (varchar)

#### 5. `job_skills_map`

Junction table resolving the Many-to-Many relationship between jobs and skills.

* `job_id` (FK -> `jobs.id`, Cascade Delete)
* `skill_id` (FK -> `skills.id`, Cascade Delete)
* *Composite Primary Key:* `(job_id, skill_id)`

---

## 🛠️ Tech Stack

* **Backend:** FastAPI (Python 3.12+)
* **Data Processing:** PySpark
* **Database:** PostgreSQL
* **Storage:** AWS S3 / MinIO (Object Storage)
* **Containerization:** Docker & Docker Compose

---

## Current Active APIs

![Swagger Docs](./docs/API.png)

## ⚙️ Getting Started

### Prerequisites

* Docker & Docker Compose
* AWS Account / LocalStack (for local S3 execution)

### Installation & Local Setup

1. **Clone the Repository:**
```bash
git clone https://github.com/yourusername/job-aggregator.git
cd job-aggregator

```


2. **Configure Environment Variables:**
Create a `.env` file in the root directory:
```env
POSTGRES_USER=postgres
POSTGRES_PASSWORD=yourpassword
POSTGRES_DB=job_aggregator_prod
DATABASE_URL=postgresql://postgres:yourpassword@localhost:5432/job_aggregator_prod
AWS_ACCESS_KEY_ID=mock_key
AWS_SECRET_ACCESS_KEY=mock_secret
S3_BUCKET_NAME=job-aggregator-bronze

```


3. **Spin up Infrastructure via Docker:**
```bash
docker-compose up -d

```


4. **Run Database Migrations:**
```bash
# Assuming Alembic is configured for FastAPI
alembic upgrade head

```


5. **Trigger the PySpark Local Processing Job:**
```bash
spark-submit --packages org.postgresql:postgresql:42.7.2 scripts/spark_silver_transform.py

```



---

## 📊 Analytics & Dashboard Goals

The frontend consumes aggregated API endpoints from FastAPI to render real-time telemetry:

* **Tech Stack Heatmaps:** Identifying which skills are spiking in mentions across all job descriptions over a rolling 30-day window.
* **Geographical Distribution:** Mapping hiring volumes by standardized cities to identify upcoming tech hubs.
* **Salary vs Experience Ranges:** Scatter plots determining market compensation relative to experience limits per tech domain.