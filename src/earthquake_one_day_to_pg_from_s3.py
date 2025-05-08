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

    CREATE SECRET dwh_postgres (
        TYPE postgres,
        HOST 'localhost',
        PORT 5432,
        DATABASE postgres,
        USER 'postgres',
        PASSWORD 'postgres'
    );

    ATTACH '' AS dwh_postgres_db (TYPE postgres, SECRET dwh_postgres);

    INSERT INTO dwh_postgres_db.ods.fct_earthquake
    (
        time,
        latitude,
        longitude,
        depth,
        mag,
        mag_type,
        nst,
        gap,
        dmin,
        rms,
        net,
        id,
        updated,
        place,
        type,
        horizontal_error,
        depth_error,
        mag_error,
        mag_nst,
        status,
        location_source,
        mag_source
    )
    SELECT
        time,
        latitude,
        longitude,
        depth,
        mag,
        magType AS mag_type,
        nst,
        gap,
        dmin,
        rms,
        net,
        id,
        updated,
        place,
        type,
        horizontalError AS horizontal_error,
        depthError AS depth_error,
        magError AS mag_error,
        magNst AS mag_nst,
        status,
        locationSource AS location_source,
        magSource AS mag_source
    FROM 's3://prod/raw/earthquake/2025-01-10/2025-02-27_00-00-00.gz.parquet';

    
    
    
    
    

    """,
)
