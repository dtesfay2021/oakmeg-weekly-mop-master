from main import main
from constants import PROJECT_ENV_VAR_NAME, S3_OUTPUT_PREFIX_ENV_VAR_NAME

def lambda_handler(event, context):
    
    # Pull variables from JSON event
    # AWS EventsBridge should parse a constant to Lambda
    project = event[PROJECT_ENV_VAR_NAME]
    S3_PREFIX = event[S3_OUTPUT_PREFIX_ENV_VAR_NAME]
    
    main(project, S3_PREFIX)
    print("Script complete")
    return