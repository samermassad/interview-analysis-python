import cv2
import numpy as np
from tqdm import tqdm
import logging
from PIL import Image
# from google_api_request import Request
from azur_api_request import Request
import video_results
from video_results import VideoResults


def analyse_file(input_file):
    # Logging
    logging.basicConfig(filename='video_analyser.log', level=logging.DEBUG)

    cap = cv2.VideoCapture(input_file)
    if not cap.isOpened():
        print("Unable to open {}, skipping...".format(input_file))
        return

    analysed_data = {}
    frame_number = 0

    previous_frame = None

    # progress bar
    frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    progress_bar = tqdm(total=frame_count, leave=False, unit="frames")

    api_request = Request()
    while cap.isOpened():
        ret, frame = cap.read()
        if (not ret) | (cv2.waitKey(1) & 0xFF == ord('q')):
            progress_bar.close()
            break
        else:
            frame_number += 1

            # Call the api
            img = Image.fromarray(frame, 'RGB')
            results = api_request.detect_faces(img)

            # Calculate camera instability
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            frame_delta = calculate_background_delta(gray, previous_frame)
            results.camera_instability = frame_delta
            previous_frame = gray

            # Store results
            analysed_data[frame_number] = results

        # update the bar
        progress_bar.update(1)

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
