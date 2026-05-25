import cv2
import mediapipe as mp

mp_hands = mp.solutions.hands
mp_draw = mp.solutions.drawing_utils

hands = mp_hands.Hands(
    max_num_hands=1,
    min_detection_confidence=0.5,
    min_tracking_confidence=0.5
)

cap = cv2.VideoCapture(0)

tip_ids = [4, 8, 12, 16, 20]

print("Show your hand to the camera.")
print("Press q to quit.")

while True:
    ret, frame = cap.read()

    if not ret:
        break

    frame = cv2.flip(frame, 1)

    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    results = hands.process(rgb)

    finger_count = 0
    gesture = "No Hand"

    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:

            mp_draw.draw_landmarks(
                frame,
                hand_landmarks,
                mp_hands.HAND_CONNECTIONS
            )

            lm = hand_landmarks.landmark

            # Thumb
            if lm[4].x < lm[3].x:
                finger_count += 1

            # Other fingers
            if lm[8].y < lm[6].y:
                finger_count += 1
            if lm[12].y < lm[10].y:
                finger_count += 1
            if lm[16].y < lm[14].y:
                finger_count += 1
            if lm[20].y < lm[18].y:
                finger_count += 1

            if finger_count == 0:
                gesture = "Fist"
            elif finger_count == 1:
                gesture = "One"
            elif finger_count == 2:
                gesture = "Two"
            elif finger_count == 5:
                gesture = "Open Palm"
            else:
                gesture = f"{finger_count} Fingers"

    cv2.putText(
        frame,
        f"Gesture: {gesture}",
        (10, 30),
        cv2.FONT_HERSHEY_SIMPLEX,
        1,
        (0, 255, 0),
        2
    )

    cv2.imshow("Hand Gesture Controller", frame)

    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

cap.release()
cv2.destroyAllWindows()
hands.close()