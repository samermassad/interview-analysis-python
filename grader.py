import constants
from video_results import VideoResults


def calculate_grade(analysed_data):
    grade = 0

    grade += calculate_angle_score(analysed_data.head_pose['roll_angle'], constants.head_pose_roll_threshold,
                                   constants.head_pose_min_value, constants.head_pose_max_value)

    grade += calculate_angle_score(analysed_data.head_pose['tilt_angle'], constants.head_pose_tilt_threshold,
                                   constants.head_pose_min_value, constants.head_pose_max_value)

    grade += 4 * analysed_data.emotions['happiness']

    grade += 4 - (4 * analysed_data.emotions['sadness'])

    grade = grade / 4

    return grade


def calculate_angle_score(angle, best_value, min_value, max_value):
    return 4 - (abs(angle - best_value) / (max_value - min_value) * 8)


if __name__ == '__main__':
    results = VideoResults(0)
    results.set_head_pose(180, -180, 0)
    emotions = {
        'happiness': 0.0,
        'sadness': 0.9
    }
    results.emotions = emotions
    print(calculate_grade(results))
