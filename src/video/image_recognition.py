import keras, os
import numpy as np

# Constants
LETTERS = {
    0:'A',
    1:'B',
    2:'C',
    3:'D',
    4:'E',
    5:'F',
    6:'G',
    7:'I',
    8:'K',
    9:'L',
    10:'M',
    11:'N',
    12:'O',
    13:'P',
    14:'Q',
    15:'R',
    16:'S',
    17:'T',
    18:'U',
    19:'V',
    20:'W',
    21:'X',
    22:'Y',
    23:'Z',
}

MODEL_DIR = os.path.join("data", "models")
MODEL_NAME = "2022-08-28_124825_e25_%80.h5"

class Recogniser():
    def __init__(self) -> None:
        self._model = keras.models.load_model(
            os.path.join(MODEL_DIR, MODEL_NAME)
        )

    def predict(self, img) -> np.ndarray:
        """ Predict which sign class is shown in the provided image. """
        return self._model(img)

    def predict_letter(self, img) -> str:
        """ Predict which letter is being signed in the provided image. """
        return LETTERS[np.argmax(self.predict(img))]
