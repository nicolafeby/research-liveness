import os
import cv2
from liveness.detector import LivenessDetector

def test_liveness_on_static_image():
    detector = LivenessDetector()

    # Path gambar relatif terhadap file test ini
    image_path = os.path.join(os.path.dirname(__file__), "sample_face.jpg")
    frame = cv2.imread(image_path)

    if frame is None:
        print(f"Gambar tidak ditemukan di: {image_path}")
        return

    result = detector.analyze(frame)

    if result["faces"]:
        print("Wajah berhasil terdeteksi!")

        # Crop wajah pertama (misal hanya menampilkan wajah utama)
        face = result["faces"][0]
        x, y, w, h = face["x"], face["y"], face["w"], face["h"]
        face_crop = frame[y:y+h, x:x+w]

        # Gambar bounding box mata pada wajah crop
        for eye in result["eyes"]:
            ex, ey, ew, eh = eye["x"], eye["y"], eye["w"], eye["h"]
            # Hanya gambar jika berada di dalam wajah crop
            if x <= ex <= x+w and y <= ey <= y+h:
                cv2.rectangle(face_crop, (ex-x, ey-y), (ex-x+ew, ey-y+eh), (255,0,0), 2)

        # Gambar bounding box senyum pada wajah crop
        for smile in result["smiles"]:
            sx, sy, sw, sh = smile["x"], smile["y"], smile["w"], smile["h"]
            if x <= sx <= x+w and y <= sy <= y+h:
                cv2.rectangle(face_crop, (sx-x, sy-y), (sx-x+sw, sy-y+sh), (0,0,255), 2)

        # Tampilkan preview hanya wajah
        cv2.imshow("Detected Face", face_crop)
        cv2.waitKey(0)
        cv2.destroyAllWindows()
    else:
        print("Tidak ada wajah yang terdeteksi.")

if __name__ == "__main__":
    test_liveness_on_static_image()
