from keras.models import load_model  # TensorFlow is required for Keras to work
import cv2  # Install opencv-python
import numpy as np
import os
from hooks.Hook import Hook

class AiDetector(Hook):
    np.set_printoptions(suppress=True)
    def __init__(self, model, class_names):
        self.model = load_model(os.path.join(os.path.dirname(__file__)) + '\\' + model)
        self.class_names = open(os.path.join(os.path.dirname(__file__)) + '\\' + class_names, "r").readlines()
        self.camera = None

    def start(self):
        self.camera = cv2.VideoCapture(0)

    def masking_detector(self):
        ret, image = self.camera.read()

        # Resize the raw image into (224-height,224-width) pixels
        image = cv2.resize(image, (224, 224), interpolation=cv2.INTER_AREA)

        # Show the image in a window
        cv2.imshow("Webcam Image", image)

        # Make the image a numpy array and reshape it to the models input shape.
        image = np.asarray(image, dtype=np.float32).reshape(1, 224, 224, 3)

        # Normalize the image array
        image = (image / 127.5) - 1

        # Predicts the model
        prediction = self.model.predict(image)
        index = np.argmax(prediction)
        class_name = self.class_names[index]
        confidence_score = prediction[0][index]

        # Print prediction and confidence score
        print("Class: ", class_name[2:], end="")
        print("Confidence Score:", str(np.round(confidence_score * 100))[:-2], "%")
        return "!1" + ":AI:" + class_name[2:-1] + "#"

    def on_message(self, feed, payload):
        print("AI: Received: " + payload.decode() + ", feed_id: " + feed)

