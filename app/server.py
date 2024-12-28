from flask import render_template, Response
from app import app
from app.camera import capture_video
from app.detector import detect_faces



import time
from PIL import Image
import numpy as np
import io
import cv2


@app.route('/')
def index():
    return render_template('index.html')

def generate_video():
    for frame in capture_video():
        processed_frame = detect_faces(frame)
        ret, jpeg = cv2.imencode('.jpg', processed_frame)
        if ret:
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + jpeg.tobytes() + b'\r\n\r\n')

@app.route('/video_feed')
def video_feed():
    return Response(generate_video(), mimetype='multipart/x-mixed-replace; boundary=frame')

def detect_faces(frame):
    # Dummy function for face detection (replace with actual implementation)
    # For example, you can use OpenCV's face detection here.
    return frame

def generate_video():
    # Open a connection to the DroidCam feed
    cap = cv2.VideoCapture("http://192.168.1.29:4747/video")

    if not cap.isOpened():
        raise RuntimeError("Could not open video feed from DroidCam")

    while True:
        # Read a frame from the video feed
        ret, frame = cap.read()

        if not ret:
            break

        # Process the frame (e.g., detect faces)
        processed_frame = detect_faces(frame)

        # Encode the frame as JPEG
        ret, jpeg = cv2.imencode('.jpg', processed_frame)

        if ret:
            # Yield the frame as a video stream with multipart encoding
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + jpeg.tobytes() + b'\r\n\r\n')

        # Optional: Add a delay to simulate frame rate (e.g., 30 fps)
        time.sleep(1 / 30)

    cap.release()  # Release the video capture when done
