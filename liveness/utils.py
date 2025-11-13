import cv2
import numpy as np

def eye_aspect_ratio(eye_points):
    """Hitung Eye Aspect Ratio (EAR) untuk deteksi kedipan."""
    A = np.linalg.norm(eye_points[1] - eye_points[5])
    B = np.linalg.norm(eye_points[2] - eye_points[4])
    C = np.linalg.norm(eye_points[0] - eye_points[3])
    return (A + B) / (2.0 * C)


def motion_detected(prev_frame, current_frame, threshold=3000):
    """Deteksi pergerakan frame dengan perbandingan frame sebelumnya."""
    if prev_frame is None:
        return False

    diff = cv2.absdiff(prev_frame, current_frame)
    gray = cv2.cvtColor(diff, cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(gray, (5, 5), 0)
    _, thresh = cv2.threshold(blur, 25, 255, cv2.THRESH_BINARY)
    motion = np.sum(thresh) / 255

    return motion > threshold
