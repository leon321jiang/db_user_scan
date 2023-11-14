# Test Conducted

1. Created all test resources via [the terraform script](../terraform_infra/infra.tf)  
    - 1 RDS MySQL instance as target db to be scannd,  
    - 2 dynamodb tables:
        - A: store a list of db (which has the 1 RDS db) and  
        - B: the users and roles retrieved from the RDS  
    - 1 sqs queue 
2. Ran [main lambd function db_user_scanner()](../lambda_source/db_user_scanner_lambda.py) (likely locally*) to initialize the setting, which
    - connected to the RDS instance and retrieve all of the DB users  
    - wrote the users to the DynamoDB table B.
3. Created new users in the rds db via [createnewuser.py](./createnewuser.py)  
4. Ran [main lambd function db_user_scanner()](../lambda_source/db_user_scanner_lambda.py) (likely locally*), which is expected to
    - add new user to the 2nd dynamodb table created above  
    - send the new user info to a SQS queue for others to consume  
\* I initially had issue to get lambda run correctly on AWS but forgot whether I finally solved it or not. However, I know the python functions were executed successfully locally for sure.
5. Observed SQS queue and saw new queue coming in with the newly added user in the RDS ![Sample SQS message](sample_sqs_message.png)

