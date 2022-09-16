# Import the used libraries
from google.cloud import vision
import firebase_admin
from firebase_admin import firestore

def analyze_emotion(event,_):
    """
    This function analyzes customer's images in order to detect emotions.
    To do so, Python accesses the Google Storage Bucket where the image is
    uploaded and then excecutes the face_detection method by Google Vision API.
    Finally, for keeping track on the results, the costumer's emotion is stored in
    a Google Firestore Data Base.
    """
    print(event) # shows the structure of the 
    vision_client = vision.ImageAnnotatorClient() # Instance of the vision client
    file_name = event["name"]  # The file name (The image to be analyzed)
    employee_name = file_name.split(".")[0] # The employee name by spliting the file name
    bucket_name = event["bucket"] # The bucket name where the image is uploaded
    blob_uri = f"gs://{bucket_name}/{file_name}"  # The image file URI in Google Storage route 
    blob_source = vision.Image(source=vision.ImageSource(image_uri=blob_uri)) # The image as a blob source that can be analyzed
    face_detection = vision_client.face_detection(image=blob_source).face_annotations     # Using the face detection method from the Google Vision API to get the face annotations
    response = face_detection[0] # Get the first face annotation found (There must be only one person in the picture)
    costumer_emotion = "Unknown" # The emotion result in case the used emotions don't match
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
    
    console_message = "The employee " + employee_name + " is " + costumer_emotion # Create the message to be displayed in the Cloud Function's Logs
    
    print(console_message) # Print the message
    app_options = {'projectId': 'soa-p1-fd'} # Set up the firebase authentication to use the Firestore Data Base
    default_app = firebase_admin.initialize_app(options=app_options) # Initialize a default app of Firebase Admin
    d_b = firestore.client() # Instance of a Firestore Client to operate the Data Base
    doc_ref = d_b.collection("employee").document("employee"+employee_name) # Create the document and the Collection
    doc_ref.set({ # Add fields to the document
        "name": employee_name,
        "emotion": costumer_emotion
    })
    firebase_admin.delete_app(default_app)# Delete the default app for not interfering with another app

    return costumer_emotion
    