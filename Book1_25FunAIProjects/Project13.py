import cv2
import numpy as np

cap = cv2.VideoCapture(0)

# HSV range for red objects
lower_red = np.array([0, 120, 70])
upper_red = np.array([10, 255, 255])

print("Show a red object to the camera.")
print("Press q to quit.")

while True:
    ret, frame = cap.read()

    if not ret:
        break

    # Flip horizontally for a mirror effect
    frame = cv2.flip(frame, 1)

    # Convert to HSV
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    # Create a binary mask
    mask = cv2.inRange(hsv, lower_red, upper_red)

    # Remove noise
    mask = cv2.GaussianBlur(mask, (5, 5), 0)

    # Find contours
    contours, _ = cv2.findContours(
        mask,
        cv2.RETR_EXTERNAL,
        cv2.CHAIN_APPROX_SIMPLE
    )

    if contours:
        # Select the largest contour
        largest = max(contours, key=cv2.contourArea)

        area = cv2.contourArea(largest)

        if area > 500:
            ((x, y), radius) = cv2.minEnclosingCircle(largest)

            center = (int(x), int(y))
            radius = int(radius)

            # Draw tracking circle
            cv2.circle(
                frame,
                center,
                radius,
                (0, 255, 0),
                2
            )

            # Draw center point
            cv2.circle(
                frame,
                center,
                5,
                (255, 0, 0),
                -1
            )

            # Display coordinates
            cv2.putText(
                frame,
                f"Center: {center}",
                (10, 30),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.8,
                (255, 255, 255),
                2
            )

            # Display area
            cv2.putText(
                frame,
                f"Area: {int(area)}",
                (10, 60),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.8,
                (255, 255, 255),
                2
            )

    cv2.imshow("Color Object Tracker", frame)
    cv2.imshow("Mask", mask)

    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

cap.release()
cv2.destroyAllWindows()