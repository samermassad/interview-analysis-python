# MIN AND MAX VALUES
detection_confidence_min_value = 0.0
detection_confidence_max_value = 1.0

camera_instability_min_value = 0.0
camera_instability_max_value = 255.0

head_pose_min_value = -180.0
head_pose_max_value = 180.0

face_position_min_value = 0.0
face_position_max_value = 0.0

emotions_min_value = 0.0
emotions_max_value = 1.0

smile_min_value = 0.0
smile_max_value = 1.0

# WEIGHTS
weights = {
    "face_count": 1.0,
    "detection_confidence": 1.0,
    "camera_instability": 1.0,
    "roll_angle": 2.0,
    "tilt_angle": 1.0,
    "pan_angle": 0.0,
    "happiness": 1.0,
    "surprise": 1.0,
    "sadness": 1.0,
    "smile": 1.0
}

# Thresholds
face_count_threshold = 1.0
detection_confidence_threshold = 1.0
camera_instability_threshold = 0.0
head_pose_roll_threshold = 40.0
head_pose_tilt_threshold = 10.0
head_pose_pan_threshold = 0.0
happiness_threshold = 1.0
sadness_threshold = 0.0
smile_threshold = 1.0
