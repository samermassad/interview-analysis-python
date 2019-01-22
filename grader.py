import constants
from video_results import VideoResults

"""
This is the grade calculator method.
It calculates a 0->4 grade from the analysed data.
To edit the formula used to calculate the grade, it's enough to add whatever wanted to the grades dictionary,
    as eventually it's values are summed with their corresponding weights. 

Args:
    analysed_data: a VideoResults instant
    
Returns:
    A number between 0 and 4 representing the weighted grade of the analysed data.

"""


def calculate_grade(analysed_data):
    grade = 0

    grades = {}

    grades['roll_angle'] = calculate_angle_score(analysed_data.head_pose['roll_angle'],
                                                 constants.head_pose_roll_threshold,
                                                 constants.head_pose_min_value, constants.head_pose_max_value)

    grades['pan_angle'] = calculate_angle_score(analysed_data.head_pose['pan_angle'], constants.head_pose_pan_threshold,
                                                constants.head_pose_min_value, constants.head_pose_max_value)

    grades['tilt_angle'] = calculate_angle_score(analysed_data.head_pose['tilt_angle'],
                                                 constants.head_pose_tilt_threshold,
                                                 constants.head_pose_min_value, constants.head_pose_max_value)

    grades['happiness'] = 4 * analysed_data.emotions['happiness']

    grades['sadness'] = 4 - (4 * analysed_data.emotions['sadness'])

    grades['surprise'] = 4 - (4 * analysed_data.emotions['surprise'])

    # print(grades)

    weighted_grades = {}
    weights_sum = 0

    for key in grades:
        if constants.weights[key] != 0:
            weighted_grades[key] = grades[key] * constants.weights[key]
            weights_sum += constants.weights[key]

    # print(weighted_grades)

    for x in weighted_grades:
        grade += weighted_grades[x]

    return grade / weights_sum


def calculate_angle_score(angle, best_value, min_value, max_value):
    return 4 - (abs(angle - best_value) / (max_value - min_value) * 8)


if __name__ == '__main__':
    results = VideoResults(0)
    results.set_head_pose(roll_angle=41, tilt_angle=-10, pan_angle=0)
    emotions = {
        'happiness': 0.7,
        'surprise': 0.9,
        'sadness': 0.2
    }
    results.emotions = emotions
    print(calculate_grade(results))
