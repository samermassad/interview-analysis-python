import cv2
import numpy as np
from tqdm import tqdm
import logging
from PIL import Image
# from google_api_request import Request
import azur_api_request as api
# from enums import Emotions
import video_results
from video_results import VideoResults


def analyse_file(input_file):
    # Logging
    logging.basicConfig(filename='video_analyser.log', level=logging.DEBUG)

    cap = cv2.VideoCapture(input_file)
    if not cap.isOpened():
        print("Unable to open {}, skipping...".format(input_file))
        # logging.warning("Unable to open {}, skipping...".format(input_file))
        return

    analysed_data = {}
    frame_number = 0

    previous_frame = None

    # progress bar
    frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    progress_bar = tqdm(total=frame_count, leave=False, unit="frames")

    # api = Request()
    while cap.isOpened():
        ret, frame = cap.read()
        if (not ret) | (cv2.waitKey(1) & 0xFF == ord('q')):
            progress_bar.close()
            break
        else:
            frame_number += 1

            # initialize results
            results = VideoResults()

            # call the api
            img = Image.fromarray(frame, 'RGB')
            # faces = api.detect_faces(img)
            faces = api.detect(img)

            number_of_faces = len(faces)

            if number_of_faces == 1:
                # only 1 face detected in the frame

                # get the only element in the list
                [face] = faces

                # calculate the camera instability
                gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
                frame_delta = calculate_background_delta(gray, previous_frame)
                previous_frame = gray

                # AZURE API
                face_attr = face['faceAttributes']

                results.detection_confidence = 1
                results.camera_instability = frame_delta
                results.face_count = number_of_faces
                results.set_head_pose(face_attr['headPose']['roll'],
                                      face_attr['headPose']['yaw'],
                                      face_attr['headPose']['pitch'])
                results.emotions = face_attr['emotion']

                # GOOGLE API
                # detection_confidence = face.detection_confidence
                #
                # results.face_count = number_of_faces
                # results.detection_confidence = detection_confidence
                # results.camera_instability = frame_delta
                # results.set_head_pose(face.roll_angle, face.pan_angle, face.tilt_angle)
                # # results.set_head_position(pnt1, pnt2)
                # results.set_emotions(face.joy_likelihood, face.sorrow_likelihood, face.anger_likelihood, face.surprise_likelihood)

                analysed_data[frame_number] = results

        # update the bar
        progress_bar.update(1)

    # print("\n")
    return video_results.calculate_average_results(analysed_data)


def calculate_background_delta(current_gray_frame, previous_frame):
    frame_delta = 0

    if previous_frame is not None:
        frame_delta = cv2.absdiff(previous_frame, current_gray_frame)

    return np.mean(frame_delta)


if __name__ == '__main__':
    average = analyse_file('D:/Desktop/VideoFiles/test_short.mp4')
    print(average.face_count)
    print(average.camera_instability)
    print(average.detection_confidence)
    print(average.emotions)
    print(average.head_pose)
