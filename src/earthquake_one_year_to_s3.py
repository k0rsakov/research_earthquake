import time

import duckdb
import pendulum

from cred import access_key, secret_key

start = pendulum.datetime(year=2024, month=1, day=1)
end = pendulum.datetime(year=2025, month=2, day=28)

interval = pendulum.interval(start, end)

list_date = []

for dt in interval.range("days"):
    list_date.append(dt.format("YYYY-MM-DD"))

for date in range(len(list_date)-1):
    print("💻download for date start: ", list_date[date])
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
                read_csv_auto('https://earthquake.usgs.gov/fdsnws/event/1/query?format=csv&starttime={list_date[date]}&endtime={list_date[date + 1]}') AS res
        ) TO 's3://prod/raw/earthquake/{list_date[date]}/{list_date[date]}_00-00-00.gz.parquet';
        """,
    )

    con.close()
    print("✅ download for date success: ", list_date[date])
    time.sleep(1)


