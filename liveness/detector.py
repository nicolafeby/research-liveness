import cv2
from cvzone.FaceMeshModule import FaceMeshDetector
import math
import time

class LivenessDetector:
    def __init__(self):
        self.detector = FaceMeshDetector(maxFaces=1)
        self.blink_count = 0
        self.last_blink_time = time.time()
        self.smile_detected = False
        self.last_mouth_ratio = 0
        self.last_eye_ratio = 0

    def analyze(self, frame):
        """Analisis frame: kedipan mata, senyum, dan pergerakan kepala"""
        frame, faces = self.detector.findFaceMesh(frame, draw=True)
        h, w, _ = frame.shape

        result = {
            "liveness": False,
            "blink_detected": False,
            "smile_detected": False,
            "face_movement": False,
        }

        if faces:
            face = faces[0]

            # Index landmark mata kiri/kanan (berdasarkan mediapipe)
            left_eye_up = face[159]
            left_eye_down = face[23]
            right_eye_up = face[386]
            right_eye_down = face[253]

            # Rasio kedipan
            left_eye_ratio = self._distance(left_eye_up, left_eye_down)
            right_eye_ratio = self._distance(right_eye_up, right_eye_down)
            eye_ratio = (left_eye_ratio + right_eye_ratio) / 2

            # Kedipan terdeteksi
            if eye_ratio < 5 and time.time() - self.last_blink_time > 0.5:
                self.blink_count += 1
                self.last_blink_time = time.time()
                result["blink_detected"] = True

            # Senyum (rasio mulut)
            left_mouth = face[61]
            right_mouth = face[291]
            top_mouth = face[0]
            bottom_mouth = face[17]

            mouth_ratio = self._distance(left_mouth, right_mouth) / (self._distance(top_mouth, bottom_mouth) + 1e-6)
            if mouth_ratio > 1.8:
                result["smile_detected"] = True
                self.smile_detected = True

            # Deteksi gerakan wajah sederhana (berdasarkan perbedaan posisi wajah)
            if abs(eye_ratio - self.last_eye_ratio) > 0.5 or abs(mouth_ratio - self.last_mouth_ratio) > 0.5:
                result["face_movement"] = True

            self.last_eye_ratio = eye_ratio
            self.last_mouth_ratio = mouth_ratio

            # Liveness aktif kalau minimal 1 aksi dilakukan
            if result["blink_detected"] or result["smile_detected"] or result["face_movement"]:
                result["liveness"] = True

        return result

    def _distance(self, p1, p2):
        """Hitung jarak Euclidean antara dua titik"""
        return math.sqrt((p1[0] - p2[0])**2 + (p1[1] - p2[1])**2)
