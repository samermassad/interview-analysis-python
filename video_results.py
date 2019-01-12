from enums import Emotions


class VideoResults:

    def __init__(self, init_value=None):
        self._face_count = init_value
        self._detection_confidence = init_value
        self._camera_instability = init_value

        self._head_pose = {
            "roll_angle": init_value,
            "pan_angle": init_value,
            "tilt_angle": init_value
        }
        # self._face_position = {
        #     1: init_value,
        #     2: init_value
        # }
        self._emotions = {}
        self._smile = 0.0

    # Face count
    @property
    def face_count(self):
        return self._face_count

    @face_count.setter
    def face_count(self, value):
        self._face_count = value

    # Detection confidence
    @property
    def detection_confidence(self):
        return self._detection_confidence

    @detection_confidence.setter
    def detection_confidence(self, value):
        self._detection_confidence = value

    # Camera instability
    @property
    def camera_instability(self):
        return self._camera_instability

    @camera_instability.setter
    def camera_instability(self, value):
        self._camera_instability = value

    # Head pose
    @property
    def head_pose(self):
        return self._head_pose

    @head_pose.setter
    def head_pose(self, value):
        self._head_pose = value

    def set_head_pose(self, roll_angle, pan_angle, tilt_angle):
        self._head_pose = {
            "roll_angle": roll_angle,
            "pan_angle": pan_angle,
            "tilt_angle": tilt_angle
        }

    # Emotions
    @property
    def emotions(self):
        return self._emotions

    @emotions.setter
    def emotions(self, value):
        self._emotions = value

    def set_emotions(self, joy_likelihood, sorrow_likelihood, anger_likelihood, surprise_likelihood):
        self._emotions = {
            Emotions.happy: joy_likelihood,
            Emotions.sorrow: sorrow_likelihood,
            Emotions.angry: anger_likelihood,
            Emotions.surprised: surprise_likelihood
        }

    # Smile
    @property
    def smile(self):
        return self._smile

    @smile.setter
    def smile(self, value):
        self._smile = value


def calculate_average_results(data):
    length = len(data)
    if length > 0:
        averages = VideoResults(0)
        for frame_number, frame_analysed_data in data.items():
            averages.face_count += frame_analysed_data.face_count / length
            averages.camera_instability += frame_analysed_data.camera_instability / length
            averages.detection_confidence += frame_analysed_data.detection_confidence / length

            # head pose
            temp = frame_analysed_data.head_pose
            for key, value in temp.items():
                temp[key] = value / length
            averages.head_pose = {k: averages.head_pose.get(k, 0) + temp.get(k, 0) for k in
                                  set(averages.head_pose) | set(temp)}

            # emotions
            temp = frame_analysed_data.emotions
            for key, value in temp.items():
                temp[key] = value / length
            averages.emotions = {k: averages.emotions.get(k, 0) + temp.get(k, 0) for k in
                                  set(averages.emotions) | set(temp)}

            # smile
            averages.smile += frame_analysed_data.smile / length
        return averages
    else:
        return None
