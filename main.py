from fastapi import FastAPI, WebSocket
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
import base64
import cv2
import numpy as np
from liveness.detector import LivenessDetector

app = FastAPI(title="Liveness Detection API")

# Serve folder web
app.mount("/web", StaticFiles(directory="web"), name="web")

detector = LivenessDetector()

@app.get("/", response_class=HTMLResponse)
def root():
    with open("web/index.html", "r", encoding="utf-8") as f:
        return f.read()

@app.websocket("/liveness")
async def liveness_stream(websocket: WebSocket):
    await websocket.accept()
    print("✅ Client connected")

    while True:
        try:
            # terima frame base64 dari client
            data = await websocket.receive_text()
            frame_data = base64.b64decode(data)
            np_arr = np.frombuffer(frame_data, np.uint8)
            frame = cv2.imdecode(np_arr, cv2.IMREAD_COLOR)

            # analisis frame
            result = detector.analyze(frame)

            # kirim hasil ke client
            await websocket.send_json(result)

        except Exception as e:
            print(f"❌ Error: {e}")
            break

    print("❌ Client disconnected")
