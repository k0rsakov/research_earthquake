SET TIMEZONE='UTC';
INSTALL httpfs;
LOAD httpfs;
SET s3_url_style = 'path';
SET s3_endpoint = 'minio:9000';
SET s3_access_key_id = 'MiMxBW99ZHwoK2kMPIwg';
SET s3_secret_access_key = 'EIIoWwB8plaw1paaSOzdZSGhIjvSa5VCjyJi9OiK';
SET s3_use_ssl = FALSE;


    SELECT
        *
    FROM
        's3://prod/raw/earthquake/*/*.gz.parquet'
