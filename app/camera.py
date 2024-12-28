import cv2

def capture_video():
    cap = cv2.VideoCapture(0)  # Use 0 for webcam or specify video source
    while True:
        ret, frame = cap.read()
        if not ret:
            break
        yield frame
    cap.release()
