import mediapipe as mp
import cv2
import time
import sys

from src import gestures, tracking, keyboard_input

DEBUG_MODE = True
sys.stdout = open('results.txt', 'w')

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

        steering_direction = gestures.get_steering_direction(landmarks, display_output=True, img=frame)
        fist = gestures.is_fist(landmarks, display_output=True, img=frame)
        open_hand = gestures.is_open(landmarks, display_output=True, img=frame)
        v = gestures.is_v(landmarks, display_output=True, img=frame)
        index = gestures.is_index_pointing(landmarks, display_output=True, img=frame)

        if DEBUG_MODE:
            print('-' * 60)
            print(f'Open Hand - {open_hand}  ;  Fist - {fist}  ;  V - {v}  ;  index - {index}  ;  direction - {steering_direction}')
            print(f'Set of pressed keys  -  {key_control.pressed_keys}')
            print(f'Brake State  -  {key_control.brake_state}')
            print()

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
        key_control.release_all_keys()

    curr_time = time.time()
    fps = int(1/(curr_time - prev_time))
    prev_time = curr_time
    cv2.putText(frame, f'FPS: {fps}', (50, 100), cv2.FONT_HERSHEY_COMPLEX, 1, (0, 255, 0), 2)

    cv2.imshow('Asphalt Hand Control', frame)
    if cv2.waitKey(1) & 0xff == ord('q'):
        print('Webcam feed ended. EXITING...')
        key_control.release_all_keys()
        break

cap.release()
cv2.destroyAllWindows()