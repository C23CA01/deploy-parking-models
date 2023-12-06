from google.cloud import storage
import requests

# Set up Google Cloud Storage client
client = storage.Client()
bucket_name = 'iotdashboard'
bucket = client.get_bucket(bucket_name)

# List objects in the GCS folder
folder_path = 'iotdashboard/CaptureData/ParkingData'
blobs = bucket.list_blobs(prefix=folder_path)

# Flask endpoints
detections_endpoint = 'http://localhost:5000/detections'
# image_endpoint = 'http://your-flask-server/image'

# Iterate over images
for blob in blobs:
    image_url = f'https://storage.googleapis.com/{bucket_name}/{blob.name}'

    # Example for the /detections endpoint
    response = requests.post(detections_endpoint, files={'images': requests.get(image_url).content})
    print(response.json())

    # Example for the /image endpoint
    # response = requests.post(image_endpoint, files={'images': requests.get(image_url).content})
    # Save the image or process the response as needed