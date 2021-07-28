# Intoduction
the purpose of this database is to combine song and log data so that the company like startup and sparkify can analyze which songs are popular and which singer is most hot. Also We can make some complicated analysis like when people tends to listen to rock music or classic music so that marketers in company can make some marketing strategies based on that.


# ETL in the project
pipeline in this project is following. 1. Create tables, 2. process song data and insert into table 3. process log data and insert into table. For the detailed part of database. For songplays table I assign song_play_id as a serial type because it should be distinctive from song and artist. And for each dim

# Schema for project

## Fact Table
Songplay records
(
    songplay_id SERIAL NOT NULL PRIMARY KEY,
    start_time TIMESTAMP,
    user_id int,
    level text,
    song_id text, 
    artist_id text,
    session_id int,
    location text,
    user_agent text
)

## Dimension Table

user_table ("""
CREATE TABLE IF NOT EXISTS users 
(
    user_id int NOT NULL PRIMARY KEY,
    first_name text,
    last_name text,
    gender char,
    level text
)
song_table ("""
CREATE TABLE IF NOT EXISTS songs 
(
    song_id text NOT NULL PRIMARY KEY,
    title text,
    artist_id text,
    year int,
    duration numeric
)

artist_table ("""
CREATE TABLE IF NOT EXISTS artists 
(
    artist_id text NOT NULL PRIMARY KEY,
    name text,
    location text,
    latitude text,
    longitude text
)

time_table ("""
CREATE TABLE IF NOT EXISTS time 
(
    start_time TIMESTAMP NOT NULL PRIMARY KEY,
    hour INT NOT NULL,
    day INT NOT NULL,
    week INT NOT NULL,
    month INT NOT NULL,
    year INT NOT NULL,
    weekday INT NOT NULL
)

# how to run the Python scripts in the Project

## Before run python files. we can test the code by using etl.ipnyb 
## 1. run create_tables.py
## 2. run etl.py

# Relavant Files

test.ipnb displays the first few rows of each table to let you check your database

create_tables.py drops and created your table

etl.ipynb read and processes a single file from song_data and log_data and loads into your tables in Jupyter notebook

etl.ipynb read and processes a single file from song_data and log_data and loads into your tables in ET

sql_queries.py containg all your sql queries and in imported into the last three files above