# Declare the Cloud Function
# This requires to compress the source code into a zip
# then we need to upload it to a bucket to storage

# Then, the source code can be accessed when creating the Cloud Function with terraform

# Generates an archive of the source code compressed as a .zip file.
data "archive_file" "source" {
    type        = "zip"
    source_dir  = "../src"
    output_path = "/tmp/function.zip"
}

# Add source code zip to the Cloud Function's bucket
resource "google_storage_bucket_object" "zip" {
    source       = data.archive_file.source.output_path
    content_type = "application/zip"

    # Append to the MD5 checksum of the files's content
    # to force the zip to be updated as soon as a change occurs
    name         = "src-${data.archive_file.source.output_md5}.zip"
    bucket       = google_storage_bucket.function_bucket.name
}

# Create the Cloud function triggered by a `Finalize` event on the bucket
resource "google_cloudfunctions_function" "function" {
    name                  = "sentiment_analysis_function"
    runtime               = "python37"  # of course changeable
    description = "When this function is excecuted an image from the Bucket is analyzed in order to find costumer emotions."

    # Get the source code of the cloud function as a Zip compression
    source_archive_bucket = google_storage_bucket.function_bucket.name
    source_archive_object = google_storage_bucket_object.zip.name

    # Must match the function name in the cloud function `main.py` source code
    entry_point           = "analyze_emotion"
    
    # The trigger is the termination event after uploading the photo on the Google Bucket
    event_trigger {
        event_type = "google.storage.object.finalize"
        resource   = "${var.project_id}-input" # Where the photo is
    }
}