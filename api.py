from abc import ABC, abstractmethod
from video_results import VideoResults

"""
Face Recognition Abstract API Class
To change the API, an API class should extend this class and implement all its abstract methods.
"""

class AbstractRequest(ABC):

    # The __init__ method
    @abstractmethod
    def __init__(self):
        pass

    # General method that calls the child's api_call method
    def detect_faces(self, image) -> VideoResults:
        faces = self.api_call(image)
        if not self.is_error(faces):
            return self.construct_results(faces)
        else:
            return None

    # The API call instantiation
    @abstractmethod
    def api_call(self, image):
        pass

    # Construct results from the API results
    @abstractmethod
    def construct_results(self, results) -> VideoResults:
        pass

    # Generalise the results so they can be understandable by the software
    @abstractmethod
    def generalise_results(self, results):
        # TODO: To be implemented
        pass

    # Check if the API returned an error
    @abstractmethod
    def is_error(self, results):
        # TODO: To be implemented
        pass
