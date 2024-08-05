import tensorflow as tf
import numpy as np
from tensorflow.keras.preprocessing.image import load_img, img_to_array


class TFLiteModel:
    def __init__(self, image_path):
        self.image_path = image_path
        self.interpreter = tf.lite.Interpreter(
            model_path=r"C:\Users\icare\Desktop\Cancer\Breast-Cancer-Detection\models\quantized_model (1).tflite"
        )
        self.interpreter.allocate_tensors()
        self.input_details = self.interpreter.get_input_details()
        self.output_details = self.interpreter.get_output_details()

    def load_and_preprocess_image(self):
        image = load_img(self.image_path, target_size=(50, 50))
        image = img_to_array(image)
        image /= 255.0
        image = np.expand_dims(image, axis=0)  # Add batch dimension
        return image

    def predict(self):
        input_data = self.load_and_preprocess_image()
        self.interpreter.set_tensor(self.input_details[0]['index'], input_data)
        self.interpreter.invoke()

        # Get the output
        output = self.interpreter.get_tensor(self.output_details[0]['index'])
        predicted_label = np.argmax(output)
        return predicted_label
