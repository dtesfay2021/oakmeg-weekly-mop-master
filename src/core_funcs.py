import json
from sqlalchemy import create_engine
import io
import os
import boto3
import psycopg2 # Needed for connection even if not called

from constants import s3_client, secret_client, S3_BUCKET, S3_TEMPLATE_KEY

def connect_db():
    """Connect to db, return tuple of engines"""
    #LOADING THE SECRETS FROM JSON
    rds_secret_name = "batch_user_access"
    rds_secret = json.loads(secret_client.get_secret_value(SecretId=rds_secret_name)['SecretString'])

    #SETTING THE VARIABLES
    dbhost = rds_secret['host']
    dbuser = rds_secret['username']
    dbpassword = rds_secret['password']
    dbdatabase = rds_secret['engine']
    dbport = rds_secret['port']
    dbreadhost = rds_secret['read_host']

    engine = create_engine('postgresql://' + dbuser + ':' + dbpassword + '@' + dbhost + ':' + str(dbport) + '/' + 'postgres')  
    read_engine = create_engine('postgresql://' + dbuser + ':' + dbpassword + '@' + dbreadhost + ':' + str(dbport) + '/' + 'postgres')  

    return engine, read_engine


def obj_to_s3(file: str, key: str):
    """Pushes any file to S3"""
    s3 = boto3.client('s3')
    with open(file, 'rb') as f:
        s3.put_object(Bucket= S3_BUCKET, Key=key, Body=f)
    pass


def retrieve_ppt_s3():
    """Retrieves ppt from S3 bucket"""
    s3_response_object = s3_client.get_object(Bucket=S3_BUCKET, Key=S3_TEMPLATE_KEY)
    object_content = s3_response_object['Body'].read()
    obj = io.BytesIO(object_content)
    return obj


# def pull_env_variable(variable_name):
#     try:
#         var = os.environ[variable_name]
#         print(f"Env variable {variable_name} found: {var}")
#         return var
    
#     except KeyError:
#         print(f"{variable_name} env variable not found. Please investigate")
    
#     except Exception as e:
#         print(f"Unknown error whilst getting {variable_name}: {e}")
