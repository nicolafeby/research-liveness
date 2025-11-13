from fastapi import FastAPI, WebSocket
import base64
import cv2
import numpy as np
from liveness.detector import LivenessDetector

app = FastAPI(title="Liveness Detection API (cvzone)")

detector = LivenessDetector()

@app.get("/")
def root():
    return {"message": "Liveness API is running 🚀"}

@app.websocket("/liveness")
async def liveness_stream(websocket: WebSocket):
    await websocket.accept()
    print("✅ Client connected to liveness stream")

    while True:
        try:
            # terima frame base64 dari client
            data = await websocket.receive_text()
            frame_data = base64.b64decode(data)
            np_arr = np.frombuffer(frame_data, np.uint8)
            frame = cv2.imdecode(np_arr, cv2.IMREAD_COLOR)

            # deteksi liveness
            result = detector.analyze(frame)

            # kirim hasil ke client
            await websocket.send_json(result)

        except Exception as e:
            print(f"❌ Error: {e}")
            break

    print("❌ Client disconnected")
