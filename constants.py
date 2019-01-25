# MIN AND MAX VALUES
min_values = {
    "face_count": 0.0,
    "detection_confidence": 0.0,
    "camera_instability": 0.0,
    "roll_angle": -180.0,
    "tilt_angle": -180.0,
    "pan_angle": -180.0,
    "emotions": 0.0,
    "smile": 0.0
}

max_values = {
    "face_count": 100.0,
    "detection_confidence": 1.0,
    "camera_instability": 255.0,
    "roll_angle": 180.0,
    "tilt_angle": 180.0,
    "pan_angle": 180.0,
    "emotions": 1.0,
    "smile": 1.0
}

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
thresholds = {
    "face_count": 1.0,
    "detection_confidence": 1.0,
    "camera_instability": 0.0,
    "roll_angle": 40.0,
    "tilt_angle": 10.0,
    "pan_angle": 0.0,
    "happiness": 1.0,
    "surprise": 1.0,
    "sadness": 0.0,
    "smile": 1.0
}
