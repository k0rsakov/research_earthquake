import duckdb

from cred import access_key, secret_key

con = duckdb.connect()

con.sql(
    f"""
    SET TIMEZONE='UTC';
    INSTALL httpfs;
    LOAD httpfs;
    SET s3_url_style = 'path';
    SET s3_endpoint = 'localhost:9000';
    SET s3_access_key_id = '{access_key}';
    SET s3_secret_access_key = '{secret_key}';
    SET s3_use_ssl = FALSE;

    COPY(
        SELECT
            *
        FROM
            read_csv_auto('https://earthquake.usgs.gov/fdsnws/event/1/query?format=csv&starttime=2025-01-10&endtime=2025-01-11') AS res
    ) TO 's3://prod/raw/earthquake/2025-01-10/2025-02-27_00-00-00.gz.parquet';
    """,
)
