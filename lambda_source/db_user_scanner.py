import boto3
import json
from datetime import datetime
from botocore.exceptions import ClientError
from db_helper import get_current_users_and_roles

# Initialize AWS SDK clients
dynamodb = boto3.resource('dynamodb')
sqs = boto3.client('sqs')

# Environment variables
#db_users_roles_table_name = os.getenv('USER_ROLE_TABLE')  # Table where user and role records are stored
#queue_url = os.getenv('SQS_QUEUE_URL')  # SQS queue URL for sending new user/role notifications
#onboarded_db_list = os.getenv('DB_LIST_TABLE')
db_users_roles_table_name = 'db_users_roles'
queue_url = 'https://sqs.us-west-2.amazonaws.com/202053868822/db-scan-notification'
onboarded_db_list = 'onboarded_db_list'

def db_user_scanner(event, context):
    # Read the list of databases from the 'onboarded_db_list' DynamoDB table
    onboarded_db_list_table = dynamodb.Table(onboarded_db_list)
    try:
        onboarded_dbs = onboarded_db_list_table.scan().get('Items', [])
    except ClientError as e:
        print(e.response['Error']['Message'])
        return {'statusCode': 500, 'body': e.response['Error']['Message']}

    # Process each onboarded database
    for db_info in onboarded_dbs:
        process_database(db_info['db_name'],db_info['db_host'], db_info['db_user'], db_info['db_password'], db_info['db_engine'])

def process_database(db_name, db_host, db_user, db_password, db_engine):
    # Retrieve the current list of users and roles from the database (mocked function)
    current_users, current_roles = get_current_users_and_roles(db_name,db_host, db_user, db_password, db_engine)

    # Access the 'db_users_roles' table
    db_users_roles_table = dynamodb.Table(db_users_roles_table_name)

    # Try to get the existing entry for the database
    try:
        response = db_users_roles_table.get_item(Key={'db_name': db_name})
        existing_entry = response.get('Item', None)
        
        # Prepare the update expression
        update_expression = "SET last_updated = :timestamp"
        expression_attribute_values = {':timestamp': datetime.now().isoformat()}
        
        # Check for new users or roles and prepare updates if necessary
        new_users, new_roles = [], []
        if existing_entry:
            new_users = list(set(current_users) - set(existing_entry.get('db_users', [])))
            new_roles = list(set(current_roles) - set(existing_entry.get('db_roles', [])))

            if new_users:
                update_expression += ", db_users = list_append(db_users, :new_users)"
                expression_attribute_values[':new_users'] = new_users
            if new_roles:
                update_expression += ", roles = list_append(roles, :new_roles)"
                expression_attribute_values[':new_roles'] = new_roles
        else:
            # If it's a new database, add all users and roles
            new_users = current_users
            new_roles = current_roles
            update_expression += ", db_users = :users, db_roles = :roles"
            expression_attribute_values[':users'] = new_users
            expression_attribute_values[':roles'] = new_roles
        
        # Update the 'db_users_roles' table with new or updated entries
        db_users_roles_table.update_item(
            Key={'db_name': db_name},
            UpdateExpression=update_expression,
            ExpressionAttributeValues=expression_attribute_values
        )
        
        # Send new users and roles to SQS queue
        if new_users or new_roles:
            message_payload = {
                'db_name': db_name,
                'new_users': new_users,
                'new_roles': new_roles
            }
            sqs.send_message(QueueUrl=queue_url, MessageBody=json.dumps(message_payload))

    except Exception as e:
        print(f"Error processing database {db_name}: {str(e)}")



# TODO to include error handling, logging, and consider pagination for large datasets.
