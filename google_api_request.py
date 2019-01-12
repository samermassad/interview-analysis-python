from api import AbstractRequest
from google.cloud import vision
import io
from video_results import VideoResults


class Request(AbstractRequest):
    def __init__(self):
        self.client = vision.ImageAnnotatorClient()

    def api_call(self, image):
        content = io.BytesIO()
        image.save(content, format='JPEG')
        content = content.getvalue()

        image = vision.types.Image(content=content)

        response = self.client.face_detection(image=image)
        faces = response.face_annotations
        return faces

    def construct_results(self, faces) -> VideoResults:
        results = VideoResults()
        number_of_faces = len(faces)

        if number_of_faces != 1:
            results.face_count = number_of_faces
            return results

        [face] = faces

        detection_confidence = face.detection_confidence

        results.face_count = number_of_faces
        results.detection_confidence = detection_confidence
        results.set_head_pose(face.roll_angle, face.pan_angle, face.tilt_angle)
        results.set_emotions(face.joy_likelihood, face.sorrow_likelihood, face.anger_likelihood, face.surprise_likelihood)

        return results

    def is_error(self, results):
        # TODO: To be implemented
        pass
