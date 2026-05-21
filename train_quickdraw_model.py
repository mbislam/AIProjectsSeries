import urllib.request
from pathlib import Path
import numpy as np
import tensorflow as tf

classes = ["cat", "house", "star", "tree"]
base_url = "https://storage.googleapis.com/quickdraw_dataset/full/numpy_bitmap"
data_dir = Path("quickdraw_data")
data_dir.mkdir(exist_ok=True)

X = []
y = []

samples_per_class = 5000

for label, name in enumerate(classes):
    file_path = data_dir / f"{name}.npy"

    if not file_path.exists():
        url = f"{base_url}/{name}.npy"
        print("Downloading:", url)
        urllib.request.urlretrieve(url, file_path)

    data = np.load(file_path)
    data = data[:samples_per_class]

    X.append(data)
    y.append(np.full(samples_per_class, label))

X = np.concatenate(X)
y = np.concatenate(y)

X = X.reshape(-1, 28, 28, 1).astype("float32") / 255.0

model = tf.keras.Sequential([
    tf.keras.layers.Input(shape=(28, 28, 1)),
    tf.keras.layers.Conv2D(32, 3, activation="relu"),
    tf.keras.layers.MaxPooling2D(),
    tf.keras.layers.Conv2D(64, 3, activation="relu"),
    tf.keras.layers.MaxPooling2D(),
    tf.keras.layers.Flatten(),
    tf.keras.layers.Dense(128, activation="relu"),
    tf.keras.layers.Dense(len(classes), activation="softmax")
])

model.compile(
    optimizer="adam",
    loss="sparse_categorical_crossentropy",
    metrics=["accuracy"]
)

model.fit(X, y, epochs=5, validation_split=0.2, batch_size=64)

model.save("drawing_model.h5")
print("Saved drawing_model.h5")