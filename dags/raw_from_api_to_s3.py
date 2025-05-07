# import time
import logging

import pendulum

from airflow import DAG

# from airflow.models import Variable
# from airflow.utils.task_group import TaskGroup
# from airflow.sensors.external_task import ExternalTaskSensor
# from airflow.operators.bash import BashOperator
from airflow.operators.empty import EmptyOperator
from airflow.operators.python import PythonOperator

# from airflow.operators.trigger_dagrun import TriggerDagRunOperator
# from airflow.providers.postgres.operators.postgres import PostgresOperator
# from airflow_clickhouse_plugin.operators.clickhouse import ClickHouseOperator
# from airflow.hooks.base import BaseHook
# from airflow.providers.amazon.aws.hooks.s3 import S3Hook
# from airflow.providers.postgres.hooks.postgres import PostgresHook
# from airflow_clickhouse_plugin.hooks.clickhouse import ClickHouseHook
from ritm_common.custom_callback import CustomNotificationAirflow


# from ritm_common.tg_operator import TelegramOperator
# from ritm_common.function_greenplum import create_stg_tmp_table_gp_pg
# from ritm_common.function_greenplum import delete_from_target_table
# from ritm_common.function_greenplum import drop_stg_tmp_table_gp_pg
# from ritm_common.function_greenplum import insert_into_target_table_from_stg_tmp_table
# from ritm_common.function_greenplum import vacuum_analyze_table_gp
# from ritm_common.function_sensors import create_external_task_sensors_from_db
# from ritm_common.local_config import NotificationMessageDAG
# from ritm_common.function_date import get_download_date

# Конфигурация DAG
OWNER = "i.korsakov"
DAG_ID = "raw_from_api_to_s3"

# Используемые таблицы в DAG
GP_TARGET_SCHEMA = "antares"
GP_TARGET_TABLE = "ods_accounts_profilemarathon"
GP_TMP_SCHEMA = "stg"
GP_TMP_TABLE = "tmp_ods_accounts_profilemarathon"
GP_ET_SCHEMA = "et"
GP_ET_TABLE = "antares_public_accounts_profilemarathon"

# Названия коннекторов к GP
GP_CONNECT_DEV = "greenplum_dwh_dev"
GP_CONNECT_PROD = "greenplum_dwh_prod"

LONG_DESCRIPTION = """
# LONG DESCRIPTION
"""

SHORT_DESCRIPTION = "SHORT DESCRIPTION"

args = {
    "owner": OWNER,
    "start_date": pendulum.datetime(2025, 1, 1, tz="Europe/Moscow"),
    "catchup": True,
    "retries": 3,
    "retry_delay": pendulum.duration(hours=1),
}

with DAG(
    dag_id=DAG_ID,
    schedule_interval="0 8 * * *",
    default_args=args,
    tags=["s3", "raw"],
    description=SHORT_DESCRIPTION,
    concurrency=1,
    max_active_tasks=1,
    max_active_runs=1,
) as dag:
    dag.doc_md = LONG_DESCRIPTION

    start = EmptyOperator(
        task_id="start",
    )

    print_airflow_context_values = PythonOperator(
        task_id="print_airflow_context_values",
        python_callable=print_airflow_context_values,
    )

    end = EmptyOperator(
        task_id="end",
    )

    start >> print_airflow_context_values >> end
