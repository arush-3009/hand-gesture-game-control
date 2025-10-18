import cv2
import mediapipe as mp
import math

def calc_distance(p1, p2):
    return math.sqrt(((p1.x - p2.x)**2) + ((p1.y - p2.y)**2))

def get_hand_size(landmarks):
    wrist = landmarks[0]
    middle_base = landmarks[9]
    return calc_distance(wrist, middle_base)

def is_fist(landmarks, display_output=False, img=None):
    if len(landmarks) == 0: return None
    wrist = landmarks[0]
    middle_finger_base = landmarks[9]
    hand_size = get_hand_size(landmarks)
    ret = True
    tips_and_thresholds = {8: 1, 12: 1, 16: 0.85, 20: 0.85}
    for fingertip in tips_and_thresholds:
        dist = calc_distance(landmarks[fingertip], wrist)
        ratio = dist/hand_size
        if ratio > tips_and_thresholds[fingertip]:
            ret = False
            break
    
    thumb_tip = landmarks[4]
    ring_knuckle = landmarks[14]
    thumb_to_ring = calc_distance(thumb_tip, ring_knuckle)
    thumb_ring_hand_size_ratio = thumb_to_ring/hand_size
    if thumb_ring_hand_size_ratio > 0.35: ret = False

    if display_output:
        if img is None:
            raise ValueError("img required when display_output=True")
        cv2.putText(img, f'Fist: {ret}', (1050, 50), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 0, 255), 2)
    
    return ret


def is_open(landmarks, display_output=False, img=None):
    if len(landmarks) == 0: return None
    wrist = landmarks[0]
    middle_finger_base = landmarks[9]
    hand_size = get_hand_size(landmarks)
    ret = True
    tips_and_thresholds = {8: 1.6, 12: 1.8, 16: 1.6, 20: 1.4}
    for fingertip in tips_and_thresholds:
        dist = calc_distance(landmarks[fingertip], wrist)
        ratio = dist/hand_size
        if ratio < tips_and_thresholds[fingertip]:
            ret = False
            break
    
    thumb_tip = landmarks[4]
    ring_knuckle = landmarks[14]
    thumb_to_ring = calc_distance(thumb_tip, ring_knuckle)
    thumb_ring_hand_size_ratio = thumb_to_ring/hand_size
    if thumb_ring_hand_size_ratio < 0.35: ret = False

    if display_output:
        if img is None:
            raise ValueError("img required when display_output=True")
        cv2.putText(img, f'Open Hand: {ret}', (950, 100), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 0, 255), 2)

    return ret


def get_steering_direction(landmarks, display_output=False, img=None):
    if len(landmarks) == 0: return 'center'
    x = landmarks[0].x
    
    LEFT_THRESHOLD = 0.42
    RIGHT_THRESHOLD = 0.57

    direction = None

    if x < LEFT_THRESHOLD:
        direction = 'left'
    elif x > RIGHT_THRESHOLD:
        direction = 'right'
    else:
        direction = 'center'
    
    if display_output:
        if img is None:
            raise ValueError("img required when display_output=True")
        cv2.putText(img, f'Direction: {direction}', (950, 150), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 0, 255), 2)

    return direction

def is_index_pointing(landmarks, display_output=False, img=None):

    if len(landmarks) == 0: return None
    hand_size = get_hand_size(landmarks)
    wrist = landmarks[0]
    tips_and_thresholds = {8: 1.65, 12: 0.8, 16: 0.8, 20: 0.8}
    ret = True
    for fingertip in tips_and_thresholds:
        dist = calc_distance(wrist, landmarks[fingertip])
        ratio = dist/hand_size
        if fingertip == 8 and ratio < tips_and_thresholds[fingertip]:
            ret = False
            break
        elif fingertip != 8 and ratio > tips_and_thresholds[fingertip]:
            ret = False
            break
        
    if display_output:
        if img is None:
            raise ValueError("img required when display_output=True")
        cv2.putText(img, f'Index Pointing: {ret}', (900, 200), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 0, 255), 2)
    
    return ret


def is_v(landmarks, display_output=False, img=None):

    if len(landmarks) == 0: return None

    hand_size = get_hand_size(landmarks)
    wrist = landmarks[0]
    tips_and_thresholds = {8: 1.7, 12: 1.7, 16: 1, 20: 1}
    ret = True

    extended_fingers = {8, 12}

    for fingertip in tips_and_thresholds:
        dist = calc_distance(wrist, landmarks[fingertip])
        ratio = dist / hand_size

        if fingertip in extended_fingers and ratio < tips_and_thresholds[fingertip]:
            ret = False
            break
        elif fingertip not in extended_fingers and ratio > tips_and_thresholds[fingertip]:
            ret = False
            break

    if display_output:
        if img is None:
            raise ValueError("img required when display_output=True")
        cv2.putText(img, f'V showing: {ret}', (900, 250), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 0, 255), 2)
        
    return ret



def is_thumbs_up(landmarks, display_output=False, img=None):
    if len(landmarks) == 0: return None

    ret = True

    hand_size = get_hand_size(landmarks)
    wrist = landmarks[0]
    thumb_tip = landmarks[4]

    y_distance = wrist.y - thumb_tip.y
    y_ratio = y_distance/hand_size

    if y_ratio < 2.0: 
        ret = False
    else:
    
        tips_and_thresholds = {8: 1.3, 12: 1.1, 16: 0.9, 20: 0.9}

        for fingertip in tips_and_thresholds:
            dist = calc_distance(wrist, landmarks[fingertip])
            ratio = dist/hand_size
            if ratio > tips_and_thresholds[fingertip]:
                ret = False
                break

    if display_output:
        if img is None:
            raise ValueError("img required when display_output=True")
        cv2.putText(img, f'Thumbs Up: {ret}', (900, 300), 
                    cv2.FONT_HERSHEY_COMPLEX, 1, (255, 0, 255), 2)

    return ret
        
