from abc import ABC, abstractmethod
from video_results import VideoResults


class AbstractRequest(ABC):

    @abstractmethod
    def __init__(self):
        pass

    def detect_faces(self, image) -> VideoResults:
        faces = self.api_call(image)
        if not self.is_error(faces):
            return self.construct_results(faces)
        else:
            return None

    @abstractmethod
    def api_call(self, image):
        pass

    @abstractmethod
    def construct_results(self, results) -> VideoResults:
        pass

    @abstractmethod
    def is_error(self, results):
        # TODO: To be implemented
        pass
