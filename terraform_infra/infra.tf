provider "aws" {
  region = "us-west-2" # Specify your AWS region
}

resource "aws_dynamodb_table" "onboarded_db_list" {
  name           = "onboarded_db_list"
  billing_mode   = "PROVISIONED"
  read_capacity  = 5
  write_capacity = 5
  hash_key       = "db_name"

  attribute {
    name = "db_name"
    type = "S"
  }

  tags = {
    Name = "onboarded_db_list"
  }
}

resource "aws_dynamodb_table" "db_users_roles" {
  name           = "db_users_roles"
  billing_mode   = "PROVISIONED"
  read_capacity  = 5
  write_capacity = 5
  hash_key       = "db_name"

  attribute {
    name = "db_name"
    type = "S"
  }

  tags = {
    Name = "db_users_roles"
  }
}


resource "aws_sqs_queue" "my_sqs_queue" {
  name = "db-scan-notification" # Name of the queue
}

resource "aws_db_instance" "my_db_instance" {
  allocated_storage       = 20
  storage_type            = "gp2"
  engine                  = "MySQL"
  engine_version          = "8.0.35"
  instance_class          = "db.t2.micro"
  db_name                    = "testrdsmysql"
  username                = var.db_username
  password                = var.db_password
  parameter_group_name    = "default.mysql8.0"
  skip_final_snapshot     = true
  publicly_accessible     = true
  backup_retention_period = 0
  identifier              = var.db_instance_identifier
}

