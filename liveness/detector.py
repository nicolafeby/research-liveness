import cv2
import numpy as np
import dlib
from liveness.utils import eye_aspect_ratio, motion_detected

class LivenessDetector:
    def __init__(self):
        self.detector = dlib.get_frontal_face_detector()
        self.predictor = dlib.shape_predictor("shape_predictor_68_face_landmarks.dat")
        self.prev_frame = None

    def detect_blink(self, landmarks):
        left_eye = landmarks[36:42]
        right_eye = landmarks[42:48]
        left_ear = eye_aspect_ratio(left_eye)
        right_ear = eye_aspect_ratio(right_eye)
        return left_ear < 0.21 and right_ear < 0.21

    def detect_smile(self, landmarks):
        mouth = landmarks[48:68]
        mouth_width = np.linalg.norm(mouth[6] - mouth[0])
        mouth_height = np.linalg.norm(mouth[3] - mouth[9])
        ratio = mouth_height / mouth_width
        return ratio > 0.35

    def detect_motion(self, frame):
        motion = motion_detected(self.prev_frame, frame)
        self.prev_frame = frame
        return motion

    def analyze(self, frame):
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = self.detector(gray)
        result = {"face_detected": False, "blink": False, "smile": False, "motion": False}

        for face in faces:
            result["face_detected"] = True
            shape = self.predictor(gray, face)
            landmarks = np.array([[p.x, p.y] for p in shape.parts()])

            result["blink"] = self.detect_blink(landmarks)
            result["smile"] = self.detect_smile(landmarks)
            result["motion"] = self.detect_motion(frame)

        return result
