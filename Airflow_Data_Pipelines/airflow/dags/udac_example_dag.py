from datetime import datetime, timedelta
import os
from airflow import DAG
from airflow.operators.dummy_operator import DummyOperator
from airflow.operators import ( CreateTableOperator, StageToRedshiftOperator, LoadFactOperator,
                                LoadDimensionOperator, DataQualityOperator)
from helpers import SqlQueries

# AWS_KEY = os.environ.get('AWS_KEY')
# AWS_SECRET = os.environ.get('AWS_SECRET')

s3_bucket = 'udacity-dend'
song_s3_key = "song_data/A/A/A"
log_s3_key = "log-data"
log_json_file = "log_json_path.json"

default_args = {
    'owner': 'udacity',
    'start_date': datetime(2021, 10, 4),
    'retries': 3,
    'depends_on_past': True,
    'retry_delay': timedelta(minutes=5),
    'email_on_failure': False,
#     'catchup': False
}

dag = DAG('udac_example_dag',
          default_args=default_args,
          description='Load and transform data in Redshift with Airflow',
          max_active_runs=1
#           schedule_interval='0 * * * *'
        )

start_operator = DummyOperator(task_id='Begin_execution',  dag=dag)

create_tables_in_redshift = CreateTableOperator(
    task_id = 'create_tables_in_redshift',
    redshift_conn_id = 'redshift',
    dag = dag
)


stage_events_to_redshift = StageToRedshiftOperator(
    task_id='Stage_events',
    dag=dag,
    redshift_conn_id = "redshift",
    aws_credential_id="aws_credentials",
    table="staging_events",
    s3_bucket = s3_bucket,
    s3_key = log_s3_key,
    file_format="JSON",
    log_json_file = log_json_file,
    provide_context=True
)

stage_songs_to_redshift = StageToRedshiftOperator(
    task_id='Stage_songs',
    dag=dag,
    redshift_conn_id = "redshift",
    aws_credential_id="aws_credentials",
    table="staging_songs",
    s3_bucket = s3_bucket,
    s3_key = song_s3_key,
    file_format="JSON",
    provide_context=True
)

load_songplays_table = LoadFactOperator(
    task_id='Load_songplays_fact_table',
    redshift_conn_id = 'redshift',
    query = SqlQueries.songplay_table_insert,
    table="public.songplays",
    truncate_table=True,
    dag=dag
)

load_user_dimension_table = LoadDimensionOperator(
    task_id='Load_user_dim_table',
    redshift_conn_id = 'redshift',
    query = SqlQueries.user_table_insert, 
    table="public.users",
    truncate_table=True,
    dag=dag
)

load_song_dimension_table = LoadDimensionOperator(
    task_id='Load_song_dim_table',
    redshift_conn_id = 'redshift',
    query = SqlQueries.song_table_insert, 
    table="public.songs",
    truncate_table=True,
    dag=dag
)

load_artist_dimension_table = LoadDimensionOperator(
    task_id='Load_artist_dim_table',
    redshift_conn_id = 'redshift',
    query = SqlQueries.artist_table_insert, 
    table="public.artists",
    truncate_table=True,
    dag=dag
)

load_time_dimension_table = LoadDimensionOperator(
    task_id='Load_time_dim_table',
    redshift_conn_id = 'redshift',
    query=SqlQueries.time_table_insert, 
    table="public.time",
    truncate_table=True,
    dag=dag
)

dq_checks=[{'check_sql': "SELECT COUNT(*) FROM users WHERE userid is null", 'expected_result': 0},
           {'check_sql': "SELECT COUNT(*) FROM songs WHERE songid is null", 'expected_result': 0}]

run_quality_checks = DataQualityOperator(
    task_id='Run_data_quality_checks',
    dag=dag,
    redshift_conn_id="redshift",
    dq_checks=dq_checks
)

end_operator = DummyOperator(task_id='Stop_execution',  dag=dag)

 
start_operator >> create_tables_in_redshift
create_tables_in_redshift >> [stage_events_to_redshift, stage_songs_to_redshift] >> load_songplays_table
load_songplays_table>>[ load_user_dimension_table,\
                       load_song_dimension_table,
                       load_artist_dimension_table,
                       load_time_dimension_table] \
>> run_quality_checks >> end_operator