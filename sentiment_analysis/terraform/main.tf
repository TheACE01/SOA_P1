# This the connection with the google provider
# This is called a pluggin in terraform's terms

provider "google" {
  project = var.project_id # The Google Cloud Project ID
  region  = var.region # The location
}