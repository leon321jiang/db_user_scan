import boto3
import json
from datetime import datetime

# Initialize AWS SDK clients
dynamodb = boto3.resource('dynamodb')
sqs = boto3.client('sqs')

sqs_queue_url = 'https://sqs.us-west-2.amazonaws.com/202053868822/db-scan-notification'

def update_users_roles_records(db_host, current_users, current_roles, db_users_roles_table_name):

    # Access the 'db_users_roles' table
    db_users_roles_table = dynamodb.Table(db_users_roles_table_name)

    # Try to get the existing entry for the database
    try:
        response = db_users_roles_table.get_item(Key={'db_host': db_host})
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
            Key={'db_host': db_host},
            UpdateExpression=update_expression,
            ExpressionAttributeValues=expression_attribute_values
        )
        
        # Send new users and roles to SQS queue
        if new_users or new_roles:
            message_payload = {
                'db_host': db_host,
                'new_users': new_users,
                'new_roles': new_roles
            }
            sqs.send_message(QueueUrl=sqs_queue_url, MessageBody=json.dumps(message_payload))

    except Exception as e:
        print(f"Error processing database {db_host}: {str(e)}")


# TODO to include error handling, logging, and consider pagination for large datasets.
