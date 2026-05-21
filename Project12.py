import cv2

face_cascade = cv2.CascadeClassifier(
    cv2.data.haarcascades +
    "haarcascade_frontalface_default.xml"
)

smile_cascade = cv2.CascadeClassifier(
    cv2.data.haarcascades +
    "haarcascade_smile.xml"
)

cap = cv2.VideoCapture(0)

print("Press q to quit.")

while True:
    ret, frame = cap.read()

    if not ret:
        break

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    faces = face_cascade.detectMultiScale(
        gray,
        scaleFactor=1.1,
        minNeighbors=5,
        minSize=(100, 100)
    )

    for (x, y, w, h) in faces:
        cv2.rectangle(
            frame,
            (x, y),
            (x + w, y + h),
            (255, 0, 0),
            2
        )

        roi_gray = gray[y:y+h, x:x+w]
        roi_color = frame[y:y+h, x:x+w]

        smiles = smile_cascade.detectMultiScale(
            roi_gray,
            scaleFactor=1.7,
            minNeighbors=20,
            minSize=(25, 25)
        )

        if len(smiles) > 0:
            cv2.putText(
                frame,
                "You are smiling!",
                (x, y - 10),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.9,
                (0, 255, 0),
                2
            )

        for (sx, sy, sw, sh) in smiles:
            cv2.rectangle(
                roi_color,
                (sx, sy),
                (sx + sw, sy + sh),
                (0, 255, 0),
                2
            )

    cv2.imshow("Smile Detector", frame)

    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

cap.release()
cv2.destroyAllWindows()