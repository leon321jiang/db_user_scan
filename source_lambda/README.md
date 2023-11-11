# AWS Lambda Functions for DynamoDB Operations

This repository contains two AWS Lambda functions for interacting with DynamoDB tables.

## Files

- `db_helper.py`: This script contains helper functions to interact with DynamoDB, such as retrieving current users and roles from a specified table.

- `db_user_scanner_lambda.py`: This script defines a Lambda function that scans a DynamoDB table for users and roles, compares the results with another table, and performs updates based on the scan results.

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