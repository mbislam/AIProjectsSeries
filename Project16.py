import cv2
import mediapipe as mp

mp_hands = mp.solutions.hands
mp_draw = mp.solutions.drawing_utils

hands = mp_hands.Hands(
    max_num_hands=1,
    min_detection_confidence=0.7,
    min_tracking_confidence=0.7
)

cap = cv2.VideoCapture(0)

print("Show a gesture to the camera.")
print("Press q to quit.")

while True:
    ret, frame = cap.read()

    if not ret:
        break

    frame = cv2.flip(frame, 1)
    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    results = hands.process(rgb)

    sign = "No Hand"

    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:

            mp_draw.draw_landmarks(
                frame,
                hand_landmarks,
                mp_hands.HAND_CONNECTIONS
            )

            lm = hand_landmarks.landmark

            # Finger states
            index_open = lm[8].y < lm[6].y
            middle_open = lm[12].y < lm[10].y
            ring_open = lm[16].y < lm[14].y
            pinky_open = lm[20].y < lm[18].y

            # Simple rule-based classifier
            if (not index_open and
                not middle_open and
                not ring_open and
                not pinky_open):
                sign = "A"

            elif (index_open and middle_open and
                  ring_open and pinky_open):
                sign = "B"

            elif (index_open and
                  not middle_open and
                  not ring_open and
                  not pinky_open):
                sign = "Hello"

            else:
                sign = "Unknown"

    cv2.putText(
        frame,
        f"Sign: {sign}",
        (10, 30),
        cv2.FONT_HERSHEY_SIMPLEX,
        1,
        (0, 255, 0),
        2
    )

    cv2.imshow(
        "Sign Language Mini Recognizer",
        frame
    )

    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

cap.release()
cv2.destroyAllWindows()
hands.close()