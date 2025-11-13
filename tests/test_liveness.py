import cv2
from liveness.detector import LivenessDetector

def test_liveness_on_static_image():
    detector = LivenessDetector()
    frame = cv2.imread("tests/sample_face.jpg")
    result = detector.analyze(frame)
    assert "face_detected" in result
