import io
import requests
import azur_cognitive_services_key as key
from api import AbstractRequest
from video_results import VideoResults

subscription_key = key.get_key()

# Request headers.
header = {
    'Content-Type': 'application/octet-stream',
    'Ocp-Apim-Subscription-Key': subscription_key,
}

api_url = "https://francecentral.api.cognitive.microsoft.com/face/v1.0/detect"


class Request(AbstractRequest):
    def __init__(self):
        pass

    def api_call(self, image):
        return self.detect(image)

    def detect(self, image, face_id=True, landmarks=False, attributes='smile,headPose,emotion'):
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

    def construct_results(self, faces) -> VideoResults:
        results = VideoResults()
        number_of_faces = len(faces)

        if number_of_faces != 1:
            results.face_count = number_of_faces
            return results

        [face] = faces

        face_attr = face['faceAttributes']

        results.detection_confidence = 1
        results.face_count = number_of_faces
        results.set_head_pose(face_attr['headPose']['roll'],
                              face_attr['headPose']['yaw'],
                              face_attr['headPose']['pitch'])
        results.emotions = face_attr['emotion']

        return results

    def generalise_results(self, results):
        # TODO: To be implemented
        pass

    def is_error(self, results):
        # TODO: To be implemented
        pass
