import boto3
from botocore.exceptions import ClientError
from .db_helper.db_helper import get_current_users_and_roles
from .dynamo_ops import update_users_roles_records

# Initialize AWS SDK clients
dynamodb = boto3.resource('dynamodb')

db_users_roles_table_name = 'db_users_roles'
onboarded_db_table_name = 'onboarded_db_list'

def db_user_scanner(event, context):
    # Read the list of databases from the 'onboarded_db_list' DynamoDB table
    onboarded_db_table = dynamodb.Table(onboarded_db_table_name)
    try:
        onboarded_dbs = onboarded_db_table.scan().get('Items', [])
    except ClientError as e:
        print(e.response['Error']['Message'])
        return {'statusCode': 500, 'body': e.response['Error']['Message']}

    # Process each onboarded database
    for db_info in onboarded_dbs:
        # Retrieve the current list of users and roles from the database
        current_users, current_roles = get_current_users_and_roles(db_info['db_host'],db_info['db_name'], db_info['db_user'], db_info['db_password'], db_info['db_engine'])

        #update records and send message to SQS as necessary
        update_users_roles_records(db_info['db_host'], current_users, current_roles, db_users_roles_table_name)
