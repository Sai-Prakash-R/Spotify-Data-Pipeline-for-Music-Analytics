# Spotify End-to-End Extract Transform Load(ETL) Pipeline

## Overview

This project aims at creating a data pipeline, extracting data from an **Spotify API** and loading data to **AWS S3** with some transformation logics to it to see data in much structered form.
Data is extracted here with the help of Python library named *Spotipy* for a Spotify playlist- "Top Songs- Global"

## Data Architecture

![Spotify E2E Data Pipeline Architecture](https://github.com/yatharthc13/spotify_E2E_etl_pipeline/blob/main/Spotify%20Project%20Data%20Pipeline.jpeg)

## Tools 

- ### Python
   
- ### Dataset- [Spotify API](https://spotipy.readthedocs.io/en/2.22.1/)

- ### Amazon Web Services

     1. Amazon S3 (Simple Storage Services): **Storage**
        - Amazon S3 provides scalable object storage, like a virtual hard drive in cloud.
          
     2. Amazon Cloudwatch: **Monitoring**
        - This AWS service is for collecting and tracking metrics, monitoring log files, and setting alarms.
          
     3. AWS Lambda: **Serverless Computing**
        - Allows you to run code without provisioning or managing servers, responding to events anf automatically scaling.
          
     4. Crawler: **Discovery**
        - Automatically discovers and organizes metadata about you data for use in AWS Glue.
          
     5. AWS Glue Data Catalog: **Metadata**
        - A centralized metadata repository that stores information about data sources, tranformations and targets.
          
     6. Athena: **Query**
        - Enables you to analyze data stored in S3 using standard SQL queries.

## Execution Process

 + ### Extract data from Spotify API and integrate it with Python
    
    - Here the data is getting extracted from Spotify API using a Python library called Spotipy. The data once extracted is then subdivided into 3 different Dataframes of Artists, Albums and Songs
    - The purpose of creating Dataframes is because the data extracted from APIs are never in readable form, they come in key-vlaue pair format.
    - So the data is categorized in different Dataframes as, a Dataframe is a 2-D data structure in which data is aligned in a tabular fashion in rows and columns.
    - Each Dataframe is created so that it gets easy reading data for analysis purpose.

      
+ ### Deploy code on AWS Lambda to extract API data
  
    - The complete code is well tested and verified to be deployed to AWS Lambda. Lambda is the first stage to enter into AWS.
    - We create the first Lambda function to extract data from API and to store the extracted data we use **S3**, for that S3 bucket is created.
    - The timeout should be increased from a default of 3 seconds or else the function might run into runtime error.
    - As many customs libraries might not be present in AWS similarly in this case *Spotipy* had to be manually uploaded to **Lambda Layer**.
    - S3 bucket is a container to store different objects in S3 as inside our bucket we have two different folders created- transformed_data and raw_data_spotify.
    - We store the raw data extacted from the API into raw_data_spotify so to be utilized later for transformation.
    - AWS capability to interact Lambda with S3 is fulfilled by **boto3** client.
      
+ ### Create another Lambda function for transformation
  
    - Now the transformation is done on the extarcted data so that cleansed and proper formatted data is loaded to S3.
    - Here the DATE data is transformed into it's proper *datetime* format.
    - Lambda function gives you freedom to add logic as to how you want your data to look and as per the data we extract from other sources we can transform it the way we want.
      
+ ### Add triggers for continuous extraction from Spotify
  
    - The API is integrated and data is extracted but to keep extracting the data at a particular rate, **AWS Cloudwatch** can be used.
    - Cloudwatch is used here as trigger to extract data let's say on daily basis
      
+ ### Store files in Amazon S3
  
    - The three dataframes created will now be used to store data in S3, the data after transformation is now made to store in form of CSV files inside our S3 bucket folder- transformed_data.
    - Inside that there are three folders named- album_data, artist_data and songs_data are created which will store the dataframe data.
    - Another trigger can be added to our tranformation Lambda function to store the data coming in on daily basis, this way the data storage is automated.
       
+ ### Generate AWS Glue crawlers to crawl CSV files and create tables
  
    - AWS Glue Crawlers are helpful in crawling the data from the source and then storing the data inside the databases.
    - Here three crawlers for artists, albums and songs data were created in order to created three tables of them.
    - Now since tables of these three datasets are created we can easily do our analysis.
      
+ ### Build analytical tables using Amazon Athena
  
    - The databases are ready to be analyzed.
    - Can see songs released in a specific year, highest number of songs inside an album across playlist, longest duration of songs,  and many more.

# Packages Installed

        pip install pandas
        pip install numpy
        pip install spotipy

# Conclusion

The amount of data in the world is huge but to understand it's trend it is very important to have an automated pipeline which can do extract, cleanse and load data into your desired database/application.

The role of a data piepline hence becomes crucial to make it easy for future analysis, this project helped us extract data effectively and efficiently and store it securely with the help of AWS services.

# For more understanding, contact me
Email me [at](yatharthc13@gmail.com) or connect with me on [LinkedIn](https://linkedin.com/in/yatharthc13)
