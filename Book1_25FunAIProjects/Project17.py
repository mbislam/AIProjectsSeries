import cv2
import pytesseract

pytesseract.pytesseract.tesseract_cmd = (
    r"C:\Program Files\Tesseract-OCR\tesseract.exe"
)

# Load image
image = cv2.imread("homework.jpg")

if image is None:
    print("Image not found.")
    exit()

# Convert to grayscale
gray = cv2.cvtColor(
    image,
    cv2.COLOR_BGR2GRAY
)

# Apply thresholding
_, thresh = cv2.threshold(
    gray,
    150,
    255,
    cv2.THRESH_BINARY
)

# Extract text
text = pytesseract.image_to_string(thresh)

print("Extracted Text:\n")
print(text)

# Save to file
with open("extracted_text.txt", "w",
          encoding="utf-8") as f:
    f.write(text)

print("\nText saved to extracted_text.txt")

# Show images
cv2.imshow("Original Image", image)
cv2.imshow("Thresholded Image", thresh)
cv2.waitKey(0)
cv2.destroyAllWindows()