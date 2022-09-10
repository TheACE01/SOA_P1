# This is the main Python function ready to be excecuted as a Cloud Function
def analyze_emotion(event, context):
    # Import the used libraries
    from google.cloud import vision

    # Instance of the vision client
    vision_client = vision.ImageAnnotatorClient()

    # The file name (The image to be analyzed)
    file_name = event["name"]

    # The employee name by spliting the file name
    employee_name = file_name.split(".")[0]
    
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

    # The emotion result in case the used emotions don't match
    costumer_emotion = "Unknown"

    # Checking what kind of emotion does the costumer have
    # The likeliness is a numeric value from 0 to 5
    # 0 means --> Very Unlikely
    # 5 means --> Very Likely
    if (response.joy_likelihood >= 3) and (response.joy_likelihood <= 5):
        costumer_emotion = "Happy"

    elif (response.anger_likelihood >= 3) and (response.anger_likelihood <= 5):
        costumer_emotion = "Angry"

    elif (response.sorrow_likelihood >= 3) and (response.sorrow_likelihood <= 5):
        costumer_emotion = "Sad"
        
    elif (response.surprise_likelihood >= 3) and (response.surprise_likelihood <= 5):
        costumer_emotion = "Surprised"

    # Create the message to be displayed in the Cloud Function's Logs
    console_message = "The employee " + employee_name + " is " + costumer_emotion

    # Print the message
    print(console_message)