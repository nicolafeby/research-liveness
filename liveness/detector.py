import cv2
import numpy as np

class LivenessDetector:
    def __init__(self):
        # load haarcascade bawaan OpenCV
        self.face_cascade = cv2.CascadeClassifier(
            cv2.data.haarcascades + 'haarcascade_frontalface_default.xml'
        )
        self.eye_cascade = cv2.CascadeClassifier(
            cv2.data.haarcascades + 'haarcascade_eye.xml'
        )
        self.mouth_cascade = cv2.CascadeClassifier(
            cv2.data.haarcascades + 'haarcascade_smile.xml'
        )

    def analyze(self, frame):
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        result = {
            "liveness": False,
            "faces": [],
            "eyes": [],
            "smiles": []
        }

        # --- Deteksi wajah ---
        faces = self.face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(80,80))
        if len(faces) == 0:
            return result

        for (x, y, w, h) in faces:
            result["faces"].append({"x": int(x), "y": int(y), "w": int(w), "h": int(h)})

            roi_gray = gray[y:y+h, x:x+w]

            # --- Kedipan mata / mata ---
            eyes = self.eye_cascade.detectMultiScale(roi_gray)
            for (ex, ey, ew, eh) in eyes:
                result["eyes"].append({"x": int(x+ex), "y": int(y+ey), "w": int(ew), "h": int(eh)})

            # --- Senyum ---
            smiles = self.mouth_cascade.detectMultiScale(roi_gray, scaleFactor=1.7, minNeighbors=20)
            for (sx, sy, sw, sh) in smiles:
                result["smiles"].append({"x": int(x+sx), "y": int(y+sy), "w": int(sw), "h": int(sh)})

        # --- Liveness sederhana: ada wajah + mata atau senyum ---
        if result["faces"] and (result["eyes"] or result["smiles"]):
            result["liveness"] = True

        return result
