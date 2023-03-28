import boto3
import datetime

today_ymd = datetime.datetime.today().strftime('%Y%m%d')

# Standard boto3 requirements
S3_BUCKET = 'atom-reporting'
S3_ASSET_BUCKET = 'saatchi-prod-cmp-file'
S3_TEMPLATE_KEY = "OAK/WEEKLY_MOP/OAKMEG_Pacing_Template.pptx"
REGION_NAME = 'us-east-1'

# AWS clients
s3_client = boto3.client('s3', region_name=REGION_NAME)
secret_client = boto3.client('secretsmanager', region_name=REGION_NAME)

# LAmbda env variables
PROJECT_ENV_VAR_NAME = 'CMP_PROJECT'
S3_OUTPUT_PREFIX_ENV_VAR_NAME = 'S3_OUTPUT_PREFIX'

# Variables for end Pwpt
LAMBDA_TMP_FILE_PATH_DIR = '/tmp/'
S3_OUTPUT_KEY = f'{today_ymd}_Weekly_MOP.pptx'