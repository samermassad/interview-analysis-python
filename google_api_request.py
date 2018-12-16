from google.cloud import vision
import io


class Request:
    def __init__(self):
        self.client = vision.ImageAnnotatorClient()

    def detect_faces(self, image):
        faces = self.api_call(image)
        # we can filter here the unwanted data
        return faces

    def api_call(self, image):
        # client = vision.ImageAnnotatorClient()

        content = io.BytesIO()
        image.save(content, format='JPEG')
        content = content.getvalue()

        image = vision.types.Image(content=content)

        response = self.client.face_detection(image=image)
        faces = response.face_annotations
        return faces
