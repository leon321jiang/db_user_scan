# Test Conducted

1. Create all test resources  
    - 1 RDS MySQL instance as target db to be scannd,  
    - 2 dynamodb tables:
        - A: store a list of db (which has the 1 RDS db) and  
        - B: the users and roles retrieved from the RDS  
    - 1 sqs queue) and lambda  
2. Create new users in the rds db via createuser.py  
3. Run main lambd function db_user_scanner()
3. Observe SQS queue and saw new queue coming in with the newly added user in the RDS ![Sample SQS message](sample_sqs_message.png)