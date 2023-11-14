# AWS Lambda Functions to scan RDS db users

This repository contains one AWS Lambda functions to scan RDS users and save it to DynamoDB tables and send delta to SQS.

## Known Issues
1. It only can retrieve users but NOT roles from MySQL db  
2. It assume the username and password are stored in a simple dynamodb table and in reality it shouldn't be that way


## Files

- `db_helper.py`: This script contains helper functions to interact with RDS, such as retrieving current users and roles.

- `db_user_scanner_lambda.py`: This script defines a Lambda function that use a function defined in db_helper.py to scan RDS users and roles, compares the results with another table, and performs updates based on the scan results.

## Setup

### Prerequisites
- AWS CLI already configured with Administrator permission
- Python 3.8 or higher
- boto3 library installed

### Deployment
Deploy these Lambda functions using the AWS CLI or the AWS Management Console. Ensure the execution role has the necessary permissions to interact with DynamoDB.

### Configuration
Make sure to set up the correct environment variables and IAM roles required for the Lambda functions to interact with AWS services.

## Usage
Invoke the Lambda functions with the appropriate event payload as required by your AWS infrastructure setup.

## IAM Permissions
The Lambda execution role needs permissions to perform the following actions:
- dynamodb:GetItem
- dynamodb:Scan
- dynamodb:UpdateItem
- dynamodb:PutItem

Ensure the role attached to the Lambda function has these permissions.

## Logging
Logging for these Lambda functions is automatically managed by AWS and can be reviewed in Amazon CloudWatch logs.

## Note
Before using these Lambda functions, replace any placeholder variables with actual values specific to your AWS environment and DynamoDB setup.
"""