# Cops Detector Processor

Cops Detector Processor is a Python-based data processing pipeline designed to extract structured vehicle information from descriptions stored in AWS S3 using Google's Gemini LLM. The extracted data is then automatically stored in a PostgreSQL database for further analysis.

## Overview

The application follows a three-step workflow:
1. **Fetch**: Retrieves JSON files containing vehicle records from an S3 bucket based on a specific date.
2. **Process**: Uses Google Gemini LLM to parse Polish descriptions and extract key details like license plates, car make/model, color, and location.
3. **Store**: Saves both the original data and the AI-extracted information into a PostgreSQL database.

## Features

- **Automated S3 Integration**: Efficiently lists and parses files from AWS S3 using `boto3`.
- **AI-Powered Extraction**: Leverages Google Gemini to transform unstructured text into structured JSON data.
- **Robust Fallback Mechanism**: Automatically tries multiple LLM models (e.g., `gemini-2.0-flash`, `gemini-1.5-flash`) if a resource limit is reached.
- **Database Persistence**: Stores comprehensive vehicle details, including image paths (local & S3), source URLs, and geographical information.
- **Logging**: Detailed logging of the processing steps for easy monitoring and debugging.

## Tech Stack

- **Language**: Python 3.x
- **Cloud**: AWS S3 (via `boto3`)
- **AI/LLM**: Google Generative AI (Gemini)
- **Database**: PostgreSQL (via `psycopg2`)
- **Utilities**: `argparse` for CLI, `dataclasses` for data modeling.

## Configuration

The application requires several environment variables to be set:

| Variable | Description                                                                     |
|----------|---------------------------------------------------------------------------------|
| `GEMINI_API_KEY` | Your Google Gemini API Key.                                                     |
| `DATABASE_URL` | PostgreSQL connection string (e.g., `postgres://user:password@host:port/dbname`). |
| `S3_BUCKET_NAME` | The name of the S3 bucket to fetch data from.                                   |
| `AWS_ACCESS_KEY_ID` | If not using IAM roles or local AWS config.                                     |
| `AWS_SECRET_ACCESS_KEY` | If not using IAM roles or local AWS config.                                     |

## Installation

1. **Clone the repository**:
   ```bash
   git clone <repository-url>
   cd cops-detector-processor
   ```

2. **Set up a virtual environment**:
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

Run the main processor by providing a date in `YYYY-MM-DD` format. This date is used as a prefix to locate files in your S3 bucket.

```bash
python main.py --date 2024-05-20
```

## Automation (GitHub Actions)

The project includes GitHub Actions workflows to automate the data processing pipeline:

### 1. Daily Processor Run (`main.yml`)
- **Schedule**: Automatically runs every day.
- **Manual Trigger**: Can be started manually via the "Actions" tab with an optional `custom_date` input (defaults to today's date).
- **Security**: Uses **OIDC (OpenID Connect)** to securely authenticate with AWS without storing long-lived credentials.

### 2. OIDC Validation (`oidc-test.yml`)
- A helper workflow used to verify the connection between GitHub Actions and AWS IAM roles.


## Database Schema

The application expects a table named `cars` with the following columns:

- `id` (Serial/Primary Key)
- `description` (Text)
- `img_url` (Text)
- `img_local_path` (Text)
- `img_s3_path` (Text)
- `current_plate_number` (Text)
- `old_plate_number` (JSONB/Text[])
- `vehicle_color` (Text)
- `voivodeship` (Text)
- `city` (Text)
- `source` (Text)
- `roads` (JSONB)
- `llm_extracted` (JSONB)
- `car_info` (Text)
- `created_at` (Timestamp - recommended)
