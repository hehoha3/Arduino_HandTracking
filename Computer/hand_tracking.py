import math

import cv2
import mediapipe as mp
import pyfirmata

board = pyfirmata.Arduino("/dev/ttyACM0")

mp_hands = mp.solutions.hands
mp_draw = mp.solutions.drawing_utils
mp_draw_styles = mp.solutions.drawing_styles

hands = mp_hands.Hands()

cap = cv2.VideoCapture(0)


def led_on():
    board.digital[8].write(1)


def led_off():
    board.digital[8].write(0)


while True:
    ret, frame = cap.read()

    imageRGB = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    result = hands.process(imageRGB)

    if result.multi_hand_landmarks:
        for hand in result.multi_hand_landmarks:
            for i, landmark in enumerate(hand.landmark):
                hight, weight, color = frame.shape

                if i == 4:
                    x, y = int(landmark.x * weight), int(landmark.y * hight)
                    p1 = (x, y)
                    cv2.circle(frame, p1, 10, [0, 0, 255], cv2.FILLED)

                if i == 8:
                    x, y = int(landmark.x * weight), int(landmark.y * hight)
                    p2 = (x, y)
                    cv2.circle(frame, p2, 10, [0, 0, 255], cv2.FILLED)

        cv2.line(frame, p1, p2, [255, 0, 0], 2)
        distance = math.sqrt((p2[0] - p1[0]) ** 2 + (p2[1] - p1[1]) ** 2)

        if distance < 80:
            led_on()
        else:
            led_off()

    cv2.imshow("Hand", frame)
    if cv2.waitKey(1) & 0xFF == ord("q"):
        break
