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
    final_grade = 0

    grades = {}

    """
    To add or edit the formula, customise the grades dictionary below.
    Please keep the formula in the comment below updated. 
    
    Current Formula is:
    
    4 - (|roll_angle - roll_angle_best_value| / (roll_angle_max_value - roll_angle_min_value) * 8) +
    4 - (|pan_angle - pan_angle_best_value| / (pan_angle_max_value - pan_angle_min_value) * 8) +
    4 - (|tilt_angle - tilt_angle_best_value| / (tilt_angle_max_value - tilt_angle_min_value) * 8) +
    4 * happiness_probability +
    4 - (4 * sadness_probability) +
    4 - (4 * surprise_probability)
    
    """

    grades['roll_angle'] = calculate_angle_score(analysed_data.head_pose['roll_angle'],
                                                 constants.thresholds['roll_angle'],
                                                 constants.min_values['roll_angle'], constants.max_values['roll_angle'])

    grades['pan_angle'] = calculate_angle_score(analysed_data.head_pose['pan_angle'], constants.thresholds['pan_angle'],
                                                constants.min_values['pan_angle'], constants.max_values['pan_angle'])

    grades['tilt_angle'] = calculate_angle_score(analysed_data.head_pose['tilt_angle'],
                                                 constants.thresholds['tilt_angle'],
                                                 constants.min_values['tilt_angle'], constants.max_values['tilt_angle'])

    grades['happiness'] = 4 * analysed_data.emotions['happiness']

    grades['sadness'] = 4 - (4 * analysed_data.emotions['sadness'])

    grades['surprise'] = 4 - (4 * analysed_data.emotions['surprise'])

    # Formula ended

    # print(grades)

    weighted_grades = {}
    weights_sum = 0

    # Calculating the weighted grades
    for key in grades:
        if constants.weights[key] != 0:
            weighted_grades[key] = grades[key] * constants.weights[key]
            weights_sum += constants.weights[key]

    # print(weighted_grades)

    # Summing weighted grades
    for x in weighted_grades:
        final_grade += weighted_grades[x] / weights_sum

    return final_grade


def calculate_angle_score(angle, best_value, min_value, max_value):
    return 4 - (abs(angle - best_value) / (max_value - min_value) * 8)


if __name__ == '__main__':
    results = VideoResults(0)
    results.set_head_pose(roll_angle=20, tilt_angle=-10, pan_angle=0)
    emotions = {
        'happiness': 0.7,
        'surprise': 0.9,
        'sadness': 0.2
    }
    results.emotions = emotions
    print(calculate_grade(results))
