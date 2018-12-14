from google.cloud import vision
import io


def detect_faces(image):
    faces = api_call(image)
    # we can filter here the unwanted data
    return faces


def api_call(image):
    client = vision.ImageAnnotatorClient()

    content = io.BytesIO()
    image.save(content, format='JPEG')
    content = content.getvalue()

    image = vision.types.Image(content=content)

    response = client.face_detection(image=image)
    faces = response.face_annotations
    return faces
