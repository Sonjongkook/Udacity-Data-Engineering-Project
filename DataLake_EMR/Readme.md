## Project - Data Lake
A music streaming startup, Sparkify, has grown their user base and song database even more and want to move their data warehouse to a data lake. Their data resides in S3, in a directory of JSON logs on user activity on the app, as well as a directory with JSON metadata on the songs in their app.

In this project, we will build an ETL pipeline for a data lake hosted on S3. We will load data from S3, process the data into analytics tables using Spark, and load them back into S3. We will deploy this Spark process on a cluster using AWS.

## ETL Pipeline
### Read data from S3

Song data: s3://udacity-dend/song_data
Log data: s3://udacity-dend/log_data
The script reads song_data and load_data from S3.

### Process data using spark(EMR) and Transforms them to create five different tables listed below :

-Fact Table
songplays - records in log data associated with song plays i.e. records with page NextSong

songplay_id, start_time, user_id, level, song_id, artist_id, session_id, location, user_agent

-Dimension Tables
users - users in the app Fields - user_id, first_name, last_name, gender, level

songs - songs in music database Fields - song_id, title, artist_id, year, duration

artists - artists in music database Fields - artist_id, name, location, lattitude, longitude

time - timestamps of records in songplays broken down into specific units Fields - start_time, hour, day, week, month, year, weekday

### Load it back to S3

Writes them to partitioned parquet files in table directories on S3.

## Process
### 1. File dl.cfg is not provided here. File contains 
```
KEY=YOUR_AWS_ACCESS_KEY
SECRET=YOUR_AWS_SECRET_KEY
```

### 2. Create EMR Cluster and configure appropriately

### 3. Move etl.py and dl.cfg to the emr cluster with ssh connection to the master node

```
ssh -i spark-cluster.pem hadoop@ec2-52-26-71-243.us-west-2.compute.amazonaws.com
```
```
scp -i spark-cluster.pem etl.py hadoop@ec2-52-26-71-243.us-west-2.compute.amazonaws.com:/home/hadoop/
```
### 4. Running spark job (Before running job make sure EMR Role have access to s3)
```
/usr/bin/spark-submit --master yarn ./etl.py
```
## Output(Spark job is succesfully implemented with emr and processed data moved to S3)
![](https://github.com/Sonjongkook/Udacity-Data-Engineering-Project/blob/main/DataLake_EMR/images/2.PNG)
![](https://github.com/Sonjongkook/Udacity-Data-Engineering-Project/blob/main/DataLake_EMR/images/3.PNG)
![](https://github.com/Sonjongkook/Udacity-Data-Engineering-Project/blob/main/DataLake_EMR/images/1.PNG)

