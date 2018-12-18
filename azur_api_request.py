import io
import requests
import azur_cognitive_services_key as key

subscription_key = key.get_key()

# Request headers.
header = {
    'Content-Type': 'application/octet-stream',
    'Ocp-Apim-Subscription-Key': subscription_key,
}

api_url = "https://westeurope.api.cognitive.microsoft.com/face/v1.0/detect"

def detect(image, face_id=True, landmarks=False, attributes='smile,headPose,emotion'):
    binary_image = io.BytesIO()
    image.save(binary_image, format='JPEG')
    binary_image = binary_image.getvalue()

    params = {
        'returnFaceId': face_id and 'true' or 'false',
        'returnFaceLandmarks': landmarks and 'true' or 'false',
        'returnFaceAttributes': attributes,
    }

    r = requests.post(api_url,
                      params=params,
                      headers=header,
                      data=binary_image)

    return r.json()
