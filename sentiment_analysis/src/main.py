# This is the main Python function ready to be excecuted as a Cloud Function
def analyze_emotion(event, context):
    # Import the used libraries
    from google.cloud import vision

    # Instance of the vision client
    vision_client = vision.ImageAnnotatorClient()

    # The file name (The image to be analyzed)
    file_name = event["name"]

    # The bucket name where the image is uploaded
    bucket_name = event["bucket"]

    # The image file URI in Google Storage route 
    blob_uri = f"gs://{bucket_name}/{file_name}"

    # The image as a blob source that can be analyzed
    blob_source = vision.Image(source=vision.ImageSource(image_uri=blob_uri)) 

    # Using the face detection method from the Google Vision API to get the face annotations
    face_detection = vision_client.face_detection(image=blob_source).face_annotations

    # Get the first face annotation found (There must be only one person in the picture)
    response = face_detection[0]

    print(response)