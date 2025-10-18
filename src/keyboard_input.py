from pynput.keyboard import Key, Controller
import time


class KeyboardController:

    def __init__(self):
        self.keyboard = Controller()
        self.pressed_keys = set()
        self.last_spin_state = False
        self.last_shockwave_state = False

    def press_key(self, k):
        if k not in self.pressed_keys:
            self.keyboard.press(k)
            self.pressed_keys.add(k)
    
    def release_key(self, k):
        if k in self.pressed_keys:
            self.keyboard.release(k)
            self.pressed_keys.remove(k)

    def handle_drift(self, gesture_active):
        if gesture_active:
            self.press_key('s')
        else:
            self.release_key('s')

    def handle_boost(self, gesture_active):
        if gesture_active:
            self.press_key(Key.space)
        else:
            self.release_key(Key.space)
    
    def handle_steering(self, gesture_result):

        if gesture_result == "left":
            self.release_key('d')
            self.press_key('a')
        elif gesture_result == "right":
            self.release_key('a')
            self.press_key('d')
        else:
            self.release_key('a')
            self.release_key('d')

    def handle_spin(self, gesture_active):
        if gesture_active and not self.last_spin_state:
            self.keyboard.press('s')
            self.keyboard.release('s')
            time.sleep(0.01)
            self.keyboard.press('s')
            self.keyboard.release('s')
        self.last_spin_state = gesture_active

        
    
    def handle_shockwave(self, gesture_active):

        if gesture_active and not self.last_shockwave_state:
            self.keyboard.press(Key.space)
            self.keyboard.release(Key.space)
            time.sleep(0.01)
            self.keyboard.press(Key.space)
            self.keyboard.release(Key.space)
        self.last_shockwave_state = gesture_active

    def release_all_keys(self):
        while self.pressed_keys:
            key = self.pressed_keys.pop()
            self.keyboard.release(key)
    


    


        
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
    
