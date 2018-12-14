import cv2
import numpy as np
import argparse
from tqdm import tqdm
import logging
from PIL import Image
import google_api_request as api
from enums import Emotions

analysed_data = {}
frame_number = 0

previous_frame = None

# progress bar
progress_bar = 0


def main():
    # Logging
    logging.basicConfig(filename='video_analyser.log', level=logging.DEBUG)

    is_file = False
    input_file = 0

    parser = argparse.ArgumentParser()
    parser.add_argument("file", help="video file location (0 for camera)")
    args = parser.parse_args()
    if args.file != '0':
        input_file = args.file
        is_file = True
        logging.debug('Analyzing file: ' + input_file)

    cap = cv2.VideoCapture(input_file)
    if not cap.isOpened():
        print("Unable to open video file or connect to camera.")
        return

    if is_file:
        frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
        print("Analysing: " + input_file)
        print("{}: {}".format("Total number of frames", frame_count))
        progress_bar = tqdm(total=frame_count)

    while cap.isOpened():
        ret, frame = cap.read()
        if (not ret) | (cv2.waitKey(1) & 0xFF == ord('q')):
            if is_file:
                progress_bar.close()
            break
        else:
            global frame_number
            # print("analysing frame: {}".format(frame_number))
            frame_number += 1

            img = Image.fromarray(frame, 'RGB')
            faces = api.detect_faces(img)

            number_of_faces = len(faces)

            if number_of_faces == 1:
                # more than one face

                # get the only element in the list
                [face] = faces

                head_pose = {
                    "roll_angle": face.roll_angle,
                    "pan_angle": face.pan_angle,
                    "tilt_angle": face.tilt_angle
                }
                detection_confidence = face.detection_confidence

                # upper left point of the face rectangle
                pnt1 = face.bounding_poly.vertices[0]

                # lower right point of the face rectangle
                pnt2 = face.bounding_poly.vertices[2]

                face_position = [pnt1, pnt2]

                gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
                frame_delta = calculate_background_delta(gray)

                emotions = {
                    Emotions.happy: face.joy_likelihood,
                    Emotions.sorrow: face.sorrow_likelihood,
                    Emotions.angry: face.anger_likelihood,
                    Emotions.surprised: face.surprise_likelihood
                }

                # detected_emotion = max(emotions, key=emotions.get)

                analysed_frame_data = {
                    'face_count': number_of_faces,
                    'detection_confidence': detection_confidence,
                    'camera_instability': frame_delta,
                    'head_pose': head_pose,
                    'face_position': face_position,
                    'emotions': emotions
                }

                analysed_data[frame_number] = analysed_frame_data

            # cv2.imshow("Preview", frame)

        if is_file:
            # update the bar
            progress_bar.update(1)

    print("\n")
    print(analysed_data)



def calculate_background_delta(gray_frame):
    global previous_frame
    frame_delta = 0

    if previous_frame is not None:
        frame_delta = cv2.absdiff(previous_frame, gray_frame)

    previous_frame = gray_frame

    return np.mean(frame_delta)


if __name__ == '__main__':
    main()
