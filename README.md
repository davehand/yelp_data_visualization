# yelp_dataset
CIS 550 Project Using Yelp Dataset

[Notes on the dataset](https://github.com/Yelp/dataset-examples)

Directories:
- csvs: original and updated csvs with desired columns
- inserts: insert scripts for tables, benchmarking code for complex queries
- django-1.7.7: django code
- django: the web application

Project Description:
- Running Django on AWS EC2
- Connecting to Oracle RDS DB and DynamoDB
- Using Yelp Dataset Challenge Data

Instructions for getting setup:
- For dataset:
  1. Download yelp dataset
  2. Use the json to csv converter script to convert the json files
  3. Use the get_cols and split_cats scripts to get the specific columns you want
  4. Use the insert_data script to create the insert data script from the data you have
  5. Run the create tables sql file and the other generated files to insert the data

- For django:
  1. Install django and cxOracle
  2. You can run 'sh runserver.sh' to start the django server
