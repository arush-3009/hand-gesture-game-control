import cv2
import time

from src import gestures, tracking, keyboard_input
from src.config import Config
from src.display import DisplayManager

# Load configuration
config = Config('config.yml')

# Initialize components
cap = cv2.VideoCapture(config.get('camera', 'device_id'))
if not cap.isOpened():
    raise OSError("Cannot access webcam")

cap.set(3, config.get('camera', 'width'))
cap.set(4, config.get('camera', 'height'))

detector = tracking.HandDetector()
key_control = keyboard_input.KeyboardController(config=config)
display = DisplayManager(config)


# FPS tracking
prev_time = 0

print('=' * 60)
print(' ' * 15 + 'HAND GESTURE GAME CONTROL')
print('=' * 60)
print('\nControls:')
print('  • Open hand          → Accelerate (W)')
print('  • Move hand L/R      → Steer (A/D)')
print('  • Make fist          → Brake/Reverse (S)')
print('  • V sign             → Drift (S)')
print('  • Point index finger → Nitro (N)')
print('\nPress "q" to quit')
print('=' * 60)
print()

try:
    while cap.isOpened():
        
        ret, frame = cap.read()
        if not ret:
            print('Webcam feed ended')
            break
        
        
        frame = cv2.flip(frame, 1)
        
       
        frame = detector.find_hands(frame, draw=False)  # Don't draw on frame
        landmarks = detector.find_pos(frame)
        
        
        gestures_data = {
            'open_hand': False,
            'fist': False,
            'v': False,
            'index': False,
            'steering_direction': 'center'
        }
        hand_x = None
        
        if landmarks:
            
            gestures_data['open_hand'] = gestures.is_open(landmarks)
            gestures_data['fist'] = gestures.is_fist(landmarks)
            gestures_data['v'] = gestures.is_v(landmarks)
            gestures_data['index'] = gestures.is_index_pointing(landmarks)
            gestures_data['steering_direction'] = gestures.get_steering_direction(landmarks)
            
            
            hand_x = landmarks[0].x
            
            # Handle controls
            if gestures_data['v']:
                key_control.handle_drift(True)
            else:
                key_control.handle_drift(False)
                if gestures_data['fist']:
                    key_control.handle_braking(True)
                else:
                    key_control.handle_braking(False)
            
            key_control.handle_acceleration(gestures_data['open_hand'])
            key_control.handle_steering(gestures_data['steering_direction'])
            key_control.handle_nitro(gestures_data['index'])
        else:
            # No hand detected
            key_control.release_all_keys()
        
        
        curr_time = time.time()
        fps = int(1 / (curr_time - prev_time)) if prev_time > 0 else 0
        prev_time = curr_time
        
        # Render display (with or without webcam based on mode)
        display_frame = display.render(
            webcam_frame=frame,
            fps=fps,
            gestures=gestures_data,
            hand_x_position=hand_x,
            pressed_keys=key_control.pressed_keys
        )
        
        
        display.show(display_frame)
        
        # Check for quit
        if cv2.waitKey(1) & 0xFF == ord('q'):
            print('\nExiting...')
            break

except KeyboardInterrupt:
    print('\nInterrupted by user')

finally:
    key_control.release_all_keys()
    cap.release()
    display.cleanup()
    print('Cleanup complete')