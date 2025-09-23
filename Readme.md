1. Create .env file with the following variables:
```
- POSTGRES_USER=<db user>
- POSTGRES_PASSWORD=<db pass>
- POSTGRES_DB=<db name>
- TABLE_NAME=<table_name>
- GEMINI_API_KEY=<api key>
- S3_BUCKET_NAME=<bucket name>
```

2.
```
docker build -t car-cron .
docker run -d --name car-cron-container car-cron
```