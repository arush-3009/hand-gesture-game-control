import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'
os.environ['TF_ENABLE_ONEDNN_OPTS'] = '0'

import warnings
warnings.filterwarnings('ignore')

import mediapipe as mp
import cv2
import time

from src import gestures, tracking, keyboard_input


cap = cv2.VideoCapture(0)
if not cap.isOpened():
    raise OSError("Cannot access Webcam.")

cap.set(3, 640)
cap.set(4, 480)

detector = tracking.HandDetector()
key_control = keyboard_input.KeyboardController()

curr_time = 0
prev_time = 0

print('*' * 15 + ' STARTING GAME CONTROL ' + '*' * 15)
print('Show open hand to accelerate (W)')
print('Move hand left/right to steer (A/D)')
print('Make fist to brake/reverse (S)')
print('Show V sign to drift (S + A/D)')
print('Point index finger for nitro (N)')
print("Press 'q' to quit")
print()

while cap.isOpened():

    ret, frame = cap.read()
    if not ret:
        print('Webcam feed ended/disrupted.')
        break

    frame = cv2.flip(frame, 1)
    frame = detector.find_hands(frame)
    landmarks = detector.find_pos(frame)

    if landmarks:
        # Detect all gestures
        steering_direction = gestures.get_steering_direction(landmarks, display_output=True, img=frame)
        fist = gestures.is_fist(landmarks, display_output=True, img=frame)
        open_hand = gestures.is_open(landmarks, display_output=True, img=frame)
        v = gestures.is_v(landmarks, display_output=True, img=frame)
        index = gestures.is_index_pointing(landmarks, display_output=True, img=frame)

        # Handle controls with priority
        # Priority 1: Drift (V sign) - overrides brake
        if v:
            key_control.handle_drift(True)
        else:
            key_control.handle_drift(False)
            # Priority 2: Brake/Reverse (only if not drifting)
            if fist:
                key_control.handle_braking(True)
            else:
                key_control.handle_braking(False)
        
        # Priority 3: Acceleration (independent)
        key_control.handle_acceleration(open_hand)
        
        # Priority 4: Steering (works with acceleration, reversing; blocked during brake/drift)
        key_control.handle_steering(steering_direction)
        
        # Priority 5: Nitro (independent)
        key_control.handle_nitro(index)
    
    else:
        # No hand detected - release everything
        key_control.release_all_keys()

    # Calculate and display FPS
    curr_time = time.time()
    fps = int(1/(curr_time - prev_time)) if prev_time > 0 else 0
    prev_time = curr_time
    cv2.putText(frame, f'FPS: {fps}', (50, 100), cv2.FONT_HERSHEY_COMPLEX, 1, (0, 255, 0), 2)

    cv2.imshow('Asphalt Hand Control', frame)
    if cv2.waitKey(1) & 0xff == ord('q'):
        print('Webcam feed ended. EXITING...')
        key_control.release_all_keys()
        break

cap.release()
cv2.destroyAllWindows()
print('👋 Goodbye! Drive safe!')