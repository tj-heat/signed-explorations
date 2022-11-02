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
MODEL_NAME = "2022-10-16_231009_e75_%91.h5"

class Recogniser():
    _MIN_RECOG = 0.85 # was 0.2

    def __init__(self) -> None:
        self._model = keras.models.load_model(
            os.path.join(MODEL_DIR, MODEL_NAME)
        )

    def predict(self, img) -> np.ndarray:
        """ Predict which sign class is shown in the provided image. """
        return self._model(img)

    def predict_letter(self, img) -> str:
        """ Predict which letter is being signed in the provided image. """
        predictions = self.predict(img)
        letter = np.argmax(predictions)
        max_val =  np.max(predictions)
        print(max_val)
        return LETTERS[letter] if max_val >= self._MIN_RECOG else None
