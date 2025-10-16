import cv2
import mediapipe as mp
import math

def calc_distance(p1, p2):
    return math.sqrt(((p1.x - p2.x)**2) + ((p1.y - p2.y)**2))

def get_hand_size(landmarks):
    wrist = landmarks[0]
    middle_base = landmarks[13]
    return calc_distance(wrist, middle_base)

def is_fist(landmarks, display_output=False, img=None):
    if len(landmarks) == 0: return None
    wrist = landmarks[0]
    middle_finger_base = landmarks[9]
    hand_size = calc_distance(middle_finger_base, wrist)
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
        cv2.putText(img, f'Fist: {ret}', (1050, 50), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 0, 255), 2)
    
    return ret


def is_open(landmarks, display_output=False, img=None):
    if len(landmarks) == 0: return None
    wrist = landmarks[0]
    middle_finger_base = landmarks[9]
    hand_size = calc_distance(middle_finger_base, wrist)
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
        cv2.putText(img, f'Open Hand: {ret}', (950, 100), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 0, 255), 2)

    return ret
