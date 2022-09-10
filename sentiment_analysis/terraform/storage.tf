# In this bucket google is going to store the code as a zip file
resource "google_storage_bucket" "function_bucket" {
    name     = "${var.project_id}-function"
    location = var.region
    force_destroy = true
}

# In this bucket google is going to store the photos.
# This resource will be used as a trigger to start the Cloud Function
resource "google_storage_bucket" "input_bucket" {
    name     = "${var.project_id}-input"
    location = var.region
    force_destroy = true
}