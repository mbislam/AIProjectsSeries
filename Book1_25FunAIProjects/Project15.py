import tkinter as tk
from PIL import Image, ImageDraw, ImageOps
import numpy as np
import tensorflow as tf

# Load trained model
model = tf.keras.models.load_model("drawing_model.h5")

# Class names
class_names = ["cat", "house", "star", "tree"]

# Create window
root = tk.Tk()
root.title("Drawing Recognition Game")

canvas_width = 280
canvas_height = 280

canvas = tk.Canvas(
    root,
    width=canvas_width,
    height=canvas_height,
    bg="white"
)
canvas.pack()

# Image for saving drawing
image = Image.new(
    "L",
    (canvas_width, canvas_height),
    color=255
)
draw = ImageDraw.Draw(image)

def paint(event):
    x1 = event.x - 8
    y1 = event.y - 8
    x2 = event.x + 8
    y2 = event.y + 8

    canvas.create_oval(
        x1, y1, x2, y2,
        fill="black",
        outline="black"
    )

    draw.ellipse(
        [x1, y1, x2, y2],
        fill=0
    )

def clear_canvas():
    canvas.delete("all")
    draw.rectangle(
        [0, 0, canvas_width, canvas_height],
        fill=255
    )
    result_label.config(text="Draw something!")

def predict():
    img = image.resize((28, 28))
    img = ImageOps.invert(img)

    arr = np.array(img) / 255.0
    arr = arr.reshape(1, 28, 28, 1)

    prediction = model.predict(arr, verbose=0)
    index = np.argmax(prediction)

    label = class_names[index]
    confidence = prediction[0][index] * 100

    result_label.config(
        text=f"I think this is a {label} "
             f"({confidence:.1f}%)"
    )

canvas.bind("<B1-Motion>", paint)

tk.Button(
    root,
    text="Predict",
    command=predict
).pack()

tk.Button(
    root,
    text="Clear",
    command=clear_canvas
).pack()

result_label = tk.Label(
    root,
    text="Draw something!"
)
result_label.pack()

root.mainloop()