# Terraform Infrastructure Setup

This Terraform configuration sets up the necessary AWS infrastructure for a cloud application.

## Configuration

The `infra.tf` file contains the Terraform configuration to set up the following AWS resources:

- DynamoDB Tables
- IAM Roles and Policies
- Lambda Functions
- CloudWatch Event Rules and Targets
- SQS Queues
- RDS Instances

## Prerequisites

- Terraform installed on your local machine.
- AWS CLI installed and configured with the necessary access credentials.

## Usage

To use this Terraform configuration:

```bash
terraform init
terraform validate
terraform apply
```