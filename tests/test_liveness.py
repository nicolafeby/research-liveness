import os
import cv2
import numpy as np
from PIL import Image
from liveness.detector import LivenessDetector

def load_image_safe(path):
    """Membaca gambar menggunakan PIL, lalu konversi ke format OpenCV."""
    try:
        pil_img = Image.open(path).convert("RGB")  # pastikan RGB
        cv_img = np.array(pil_img)
        # PIL pakai format RGB, OpenCV pakai BGR
        cv_img = cv2.cvtColor(cv_img, cv2.COLOR_RGB2BGR)
        return cv_img
    except Exception as e:
        print("Gagal membaca gambar dengan PIL:", e)
        return None

def test_liveness_on_static_image():
    detector = LivenessDetector()

    # Path gambar relatif terhadap file test ini
    image_path = os.path.join(os.path.dirname(__file__), "sample_face.jpg")
    image_path = os.path.abspath(image_path)
    print("Path gambar:", image_path)

    if not os.path.exists(image_path):
        print("File gambar tidak ditemukan!")
        return

    frame = load_image_safe(image_path)
    if frame is None:
        print("Gagal membaca gambar! Pastikan format JPG/PNG valid.")
        return

    result = detector.analyze(frame)

    if result["faces"]:
        print("Wajah berhasil terdeteksi!")

        # Crop wajah pertama
        face = result["faces"][0]
        x, y, w, h = face["x"], face["y"], face["w"], face["h"]
        face_crop = frame[y:y+h, x:x+w]

        # Gambar bounding box mata
        for eye in result["eyes"]:
            ex, ey, ew, eh = eye["x"], eye["y"], eye["w"], eye["h"]
            if x <= ex <= x+w and y <= ey <= y+h:
                cv2.rectangle(face_crop, (ex-x, ey-y), (ex-x+ew, ey-y+eh), (255,0,0), 2)

        # Gambar bounding box senyum
        for smile in result["smiles"]:
            sx, sy, sw, sh = smile["x"], smile["y"], smile["w"], smile["h"]
            if x <= sx <= x+w and y <= sy <= y+h:
                cv2.rectangle(face_crop, (sx-x, sy-y), (sx-x+sw, sy-y+sh), (0,0,255), 2)

        # Tampilkan preview wajah
        cv2.imshow("Detected Face", face_crop)
        cv2.waitKey(0)
        cv2.destroyAllWindows()
    else:
        print("Tidak ada wajah yang terdeteksi.")

if __name__ == "__main__":
    test_liveness_on_static_image()
