import mediapipe as mp
import cv2

from src import gestures, tracking


cap = cv2.VideoCapture(0)
if not cap.isOpened():
    raise OSError("Cannot access Webcam.")

detector = tracking.HandDetector()

while cap.isOpened():

    ret, frame = cap.read()
    if not ret:
        print('Webcam feed ended/disrupted.')
        break

    frame = cv2.flip(frame, 1)

    frame = detector.find_hands(frame)
    landmarks = detector.find_pos(frame)
    fist = gestures.is_fist(landmarks, display_output=True, img=frame)
    open_hand = gestures.is_open(landmarks, display_output=True, img=frame)

    cv2.imshow('Webcam', frame)
    if cv2.waitKey(1) & 0xff == ord('q'):
        print('Webcam feed ended. EXITING...')
        break

cap.release()
cv2.destroyAllWindows()
