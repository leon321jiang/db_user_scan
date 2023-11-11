variable "db_password" {
  description = "The password for the RDS database"
  type        = string
  // It's recommended to not provide a default value for sensitive variables
}

variable "db_instance_identifier" {
  description = "The identifier for the RDS instance"
  type        = string
  default     = "mydbinstance"
}

variable "db_username" {
  description = "Username for the RDS database"
  type        = string
  default     = "db_admin"
}

// Add any other variables you wish to parameterize
