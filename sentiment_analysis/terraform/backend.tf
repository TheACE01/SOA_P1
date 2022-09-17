# Defines where terraform is going to storage the state of the infraestructure

# Using Terraform Cloud Workspace to store the terraform state and share it with the team
# The workspace excecution is set up local, thus, Terraform Cloud just store the terraform states
terraform {
  backend "gcs" {
    bucket = "tfstate-bucket-soa"
    prefix = "/terraform.tfstate"
  }
}