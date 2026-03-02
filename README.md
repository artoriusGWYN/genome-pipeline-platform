# Genome Pipeline Platform

## Overview

Genome Pipeline Platform is a Django-based web application designed to allow biologists to run, monitor, and compare bacterial genome assembly and annotation pipelines directly from a web browser.

The platform integrates Nextflow workflows (currently supporting `nf-core/bacass`) and stores run parameters and results in a structured database. It also includes a run comparison feature based on QUAST and Prokka outputs.

Asynchronous task execution is handled using Celery, allowing long-running pipeline processes to execute in the background without blocking the web server.

⚠️ The platform is currently under active development.  
Feedback and suggestions are welcome at: **saad_didouz@outlook.fr**

---

## Requirements

Before running the platform, make sure the following tools are installed:

- Python 3.9+
- Django
- Celery
- Redis (as message broker for Celery)
- Nextflow
- Java (required for Nextflow)
- Docker or Singularity (recommended for nf-core pipelines)

Make sure Redis server is running before starting Celery.

---

## How to Run the Platform

### 1️⃣ Start Redis

In a terminal:

redis-server

### 2️⃣ Start Celery Worker

Open a first terminal and run:

celery -A genome worker --loglevel=info

### 3️⃣ Start the Django Server

Open a second terminal and run:

python manage.py runserver

The platform will be accessible at:

http://127.0.0.1:8000/
