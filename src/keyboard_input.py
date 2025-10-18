import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'
os.environ['TF_ENABLE_ONEDNN_OPTS'] = '0'

import warnings
warnings.filterwarnings('ignore')

from pynput.keyboard import Key, Controller
import time



class KeyboardController:

    def __init__(self):
        self.keyboard = Controller()
        self.pressed_keys = set()
        self.brake_state = None
        self.last_brake_state = None
        self.just_braking_state_set_time = 0
        self.last_direction = 'center'
        self.direction_change = False
    
    def press_key(self, k):
        if k not in self.pressed_keys:
            self.keyboard.press(k)
            self.pressed_keys.add(k)
    
    def release_key(self, k):
        if k in self.pressed_keys:
            self.keyboard.release(k)
            self.pressed_keys.remove(k)
    
    def release_all_keys(self):
        while self.pressed_keys:
            key = self.pressed_keys.pop()
            self.keyboard.release(key)

    def handle_acceleration(self, gesture_active):
        if gesture_active:
            self.press_key('w')
        else:
            self.release_key('w')

    # def handle_acceleration_direction(self, direction):

    #     is_accelerating = 'w' in self.pressed_keys

    #     if is_accelerating:

    #         if self.last_direction != direction:
    #             self.direction_change = True
    #         else:
    #             self.direction_change = False

    #         if direction == 'center':
    #             self.release_key('a')
    #             self.release_key('d')
    #         elif direction == 'left':
    #             if self.direction_change:
    #                 self.release_key('w')
                
    #             self.release_key('d')
    #             self.press_key('a')
    #         elif direction == 'right':
    #             if self.direction_change:
    #                 self.release_key('w')
                
    #             self.release_key('a')
    #             self.press_key('d')


    def handle_brake(self, gesture_active):
        if gesture_active:
            if self.last_brake_state != 'just_braking':
                self.brake_state = 'just_braking'
                self.just_braking_state_set_time = time.time()
                self.release_key('a')
                self.release_key('d')
            else:
                curr_time = time.time()
                if curr_time - self.just_braking_state_set_time > 2:
                    self.brake_state = 'reversing'

            self.last_brake_state = self.brake_state
            
            self.press_key('s')
        else:
            self.release_key('s')

    def handle_nitro(self, gesture_active):
        if gesture_active:
            self.press_key(Key.space)
        else:
            self.release_key(Key.space)
    
    def handle_drift(self, gesture_active):
        if gesture_active:
            self.press_key('s')
        else:
            self.release_key('s')
    
    def handle_steering(self, steering_direction):
        if self.brake_state == 'just_braking': 
            self.release_key('a')
            self.release_key('d')
            self.last_direction = None
            self.direction_change = False
        else:
            
            if self.last_direction != steering_direction:
                self.direction_change = True
            else:
                self.direction_change = False

            if steering_direction == 'left':
                if self.direction_change:
                    self.release_key('w')
                self.release_key('d')
                self.press_key('a')
            elif steering_direction == "right":
                if self.direction_change:
                    self.release_key('w')
                self.release_key('a')
                self.press_key('d')
            else:
                self.release_key('a')
                self.release_key('d')
            
            self.last_direction = steering_direction

            


# class KeyboardController:

#     def __init__(self):
#         self.keyboard = Controller()
#         self.pressed_keys = set()
#         self.last_spin_state = False
#         self.last_shockwave_state = False

#     def press_key(self, k):
#         if k not in self.pressed_keys:
#             self.keyboard.press(k)
#             self.pressed_keys.add(k)
    
#     def release_key(self, k):
#         if k in self.pressed_keys:
#             self.keyboard.release(k)
#             self.pressed_keys.remove(k)

#     def handle_drift(self, gesture_active):
#         if gesture_active:
#             self.press_key('s')
#         else:
#             self.release_key('s')

#     def handle_boost(self, gesture_active):
#         if gesture_active:
#             self.press_key(Key.space)
#         else:
#             self.release_key(Key.space)
    
#     def handle_steering(self, gesture_result):

#         if gesture_result == "left":
#             self.release_key('d')
#             self.press_key('a')
#         elif gesture_result == "right":
#             self.release_key('a')
#             self.press_key('d')
#         else:
#             self.release_key('a')
#             self.release_key('d')

#     def handle_spin(self, gesture_active):
#         if gesture_active and not self.last_spin_state:
#             self.keyboard.press('s')
#             self.keyboard.release('s')
#             time.sleep(0.05)
#             self.keyboard.press('s')
#             self.keyboard.release('s')
#         self.last_spin_state = gesture_active

        
    
#     def handle_shockwave(self, gesture_active):

#         if gesture_active and not self.last_shockwave_state:
#             self.keyboard.press(Key.space)
#             self.keyboard.release(Key.space)
#             time.sleep(0.05)
#             self.keyboard.press(Key.space)
#             self.keyboard.release(Key.space)
#         self.last_shockwave_state = gesture_active

#     def release_all_keys(self):
#         while self.pressed_keys:
#             key = self.pressed_keys.pop()
#             self.keyboard.release(key)
    


    


        
if __name__ == '__main__':

    kc = KeyboardController()
    kc.press_key(Key.shift)
    print(kc.pressed_keys) 

    kc.press_key('a')
    print(kc.pressed_keys)

    print(f'Does the state set have key "shift" ? : {Key.shift in kc.pressed_keys}\n')

    kc.release_key('a')
    print(kc.pressed_keys)
    kc.release_key(Key.shift)
    
    
    kc.press_key(Key.space)
    kc.release_key(Key.space)
    time.sleep(0.01)
    kc.press_key(Key.space)
    kc.release_key(Key.space)
    
