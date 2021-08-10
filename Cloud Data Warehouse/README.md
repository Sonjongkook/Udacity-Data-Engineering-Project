##  Discuss the purpose of this database in context of the startup, Sparkify, and their analytical goals.
 Sparkify has grown their user base and song database and want to move their processes and data onto the cloud. Their data exists in S3, in a directory of JSON logs on user activity on the app, as well as a directory with JSON metadata on the songs in their app.

Task is to build an ETL Pipeline that extracts their data from S3, staging it in Redshift and then transforming data into a set of Dimensional and Fact Tables for their Data Analytics Team to continue finding Insights to what songs their users are listening to.

## State and justify your database schema design and ETL pipeline.

### Database Schema
1. FIRST We need to finish up sql_queries.py
2. CREATE stging tables which are staging_events and staging_songs, For this tables, we can just set each field based on the 
    data format of each log and song dataset.
3. CREATE analystic tables in redshift(dimensional table and fact table). In here We need to set the sortkey, distkey 
    to implement optimizing query. I tried to select distkey which is not skewed in the data and select join column as
    sortkey to get better performance on joining tables.
4. Using copy command to load data from s3 to staging table. In this process, We need to careful about JSON format.
5. Using copy command to load data from staging table to redshift analystic table. When it comes to fact table, we need to
    join two staging table and load from there.
6. Test by running create_tables.py and checking the table schemas in your redshift database.


### ETL pipeline
1. load data from s3 buckets to the staging tables in redshift(staging_event, staging_song)
2. After succesfully loading into stagigng table then insert in to analystic tables in redshift
3. We can test this process by implementing create_tables.py and etl.py in row. 
4. Delete redshift cluster and Iam Role Once finished 1,2,3

### Instruction For Project
1. Import all libraries
2. Wrie Configuration of AWS
3. Using the bucket, can check whether files log files and song data files are present
4. We assume that redshift cluster and Iam role are already created
5. run python create_tables.py on terminal
6. run python etl.py on terminal
7. to check out that etl process is successful, run test.ipynb

### Provide example queries and results for song play analysis
I used selec and count query to show that datas are succesfully loaded into tables.
One can find out the result of queries in test.ipynb

EX)
SELECT * FROM dim_user LIMIT 10;
SELECT COUNT(*) FROM dim_user;