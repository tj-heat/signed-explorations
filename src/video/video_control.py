from turtle import width
from typing import Tuple

import cv2
import numpy as np

from src.video.image_processing import Recogniser

CAPTURING = False # Temp const for feature enabling
DEFAULT_WINDOW = "Camera Capture"

# Functions
def add_roi(
    img: np.ndarray, 
    roi: Tuple[Tuple[int, int], Tuple[int, int]], 
    colour: Tuple[int, int, int] = (255, 0, 255), # Magenta
    width: int = 2
) -> None:
    """ Draws the ROI to a given frame. 
    
    Params:
        img (ndarray): The frame to add the ROI to.
        roi (Tuple): A tuple containing two tuples, which are the x, y position 
            of the top-left and bottom right ROI corners, respectively.
        colour (Tuple): The RGB values (0-255) to draw the ROI with
        width (int): The pixel width of the ROI
    """
    tl, br = roi
    cv2.rectangle(img, tl, br, colour, width)

def get_image_roi(
    img: np.ndarray, 
    roi: Tuple[Tuple[int, int], Tuple[int, int]]
) -> np.ndarray:
    """ Crops an image to the ROI region TODO"""
    (left, top), (right, bottom) = roi
    return img[top:bottom, left:right]

def get_image_gray(img: np.ndarray):
    """ TODO """
    return cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

def get_image_blur(img: np.ndarray):
    """ TODO """
    return cv2.GaussianBlur(img, (9, 9), 0)

def get_image_diff(img: np.ndarray, ref: np.ndarray):
    """ TODO """
    return cv2.absdiff(ref.astype("uint8"), img)

def get_image_binary(img: np.ndarray, thresh: int):
    """ TODO """
    _, binary = cv2.threshold(img, thresh, 255, cv2.THRESH_BINARY)
    return binary

def preprocess_image(
    img: np.ndarray, 
    roi: Tuple[Tuple[int, int], Tuple[int, int]]
):
    """ TODO """
    crop = get_image_roi(img, roi)
    gray = get_image_gray(crop)
    blur = get_image_blur(gray)
    return blur

def process_hand_image(img: np.ndarray, ref: np.ndarray, thresh: int):
    """ TODO """
    diff = get_image_diff(img, ref)
    binary = get_image_binary(diff, thresh)
    return binary

def process_model_image(img: np.ndarray):
    """ TODO """
    # Make 64x64
    scaled = cv2.resize(img, (64, 64))
    # Convrt grayscale to RGB
    coloured = cv2.cvtColor(scaled, cv2.COLOR_GRAY2RGB)
    # Turn into array of 1x64x64 with three colour channels
    shaped = np.reshape(coloured, (1, coloured.shape[0], coloured.shape[1], 3))
    return shaped

# TODO Turn each step of the model generation into a function.

def show_image_windowed(img: np.ndarray, window: str = DEFAULT_WINDOW) -> None:
    """ Display an image in a window separate to the game window. """
    cv2.imshow(window, img)
    cv2.waitKey(1)

# Classes
class CameraControl():
    ROI_WIDTH = 200
    ROI_HEIGHT = 200

    def __init__(self) -> None:
        self._cam = self.get_cam()
        self._width = self._cam.get(cv2.CAP_PROP_FRAME_WIDTH)
        self._height = self._cam.get(cv2.CAP_PROP_FRAME_HEIGHT)
        self._background = None

    def create_background(self, weight: int = 0.5) -> None:
        """ Generates an accumulated average background for differencing TODO """
        roi = self.get_roi()

        # Initial background
        self._background = preprocess_image(self.read_cam(), roi) \
            .astype("float")

        # Generate accumulated average
        for _ in range(60):
            # # At 60fps this will take one second
            frame = preprocess_image(self.read_cam(), roi)
            cv2.accumulateWeighted(frame, self._background, weight)
    
    def get_cam(self, index: int = 0) -> cv2.VideoCapture:
        """ (VideoCapture) Returns the first listed video capture object. 
        
        Params:
            index (int): The camera index to capture. Defaults to 0.

        Returns:
            (VideoCapture) The retreived video caputure object.

        Raises:
            (Exception) if the camera at the used index does not exist/ is not
                captured.
        """
        # Attempt to capture camera as on windows
        cam = cv2.VideoCapture(index, cv2.CAP_DSHOW)
        if not cam.isOpened():
            # Attempt to capture camera with any API
            cam = cv2.VideoCapture(index)

        # If still no success, throw exception
        if not cam.isOpened():
            raise Exception("Could not open camera")

        return cam

    def get_dimensions(self) -> Tuple[float, float]:
        """ Returns the camera's width and height as floats in a tuple """
        return (self._width, self._height)

    def get_roi(self) -> Tuple[Tuple[int, int], Tuple[int, int]]:
        """ Returns a tuple containing the top left and bottom right corners of 
            the ROI.
        """
        x_mid, y_mid = [int(dim / 2) for dim in self.get_dimensions()]
        x_offset = self.ROI_WIDTH // 2
        y_offset = self.ROI_HEIGHT // 2

        return (
            (x_mid - x_offset, y_mid - y_offset),   # left, top
            (x_mid + x_offset, y_mid + y_offset)    # right, bottom
        )

    def _get_background_diff(self, img: np.ndarray, thresh: int):
        """ TODO """
        if self._background is None:
            raise ValueError("No background image for reference")

        if self._background.shape != img.shape:
            raise ValueError("Provided image is not the correct shape/size")

        return process_hand_image(img, self._background, thresh)

    def get_hand_segment(self, thresh: int = 25):
        """ TODO """
        img = preprocess_image(self.read_cam(), self.get_roi())
        binary = self._get_background_diff(img, thresh)
        
        contours, _ = cv2.findContours(
            binary, 
            cv2.RETR_EXTERNAL, 
            cv2.CHAIN_APPROX_SIMPLE
        )
    
        if len(contours):
            largest_contour = max(contours, key=cv2.contourArea)
            return (binary, largest_contour)

    def read_cam(self) -> np.ndarray:
        """ Retrieve a single frame from a captured camera. 
        
        Returns:
            (ndarray) The captured frame from the camera.

        Raises:
            (Exception) if the camera cannot be read from.
        """
        success, frame = self._cam.read()

        if not success:
            raise Exception("Could not capture frame from camera")

        return cv2.flip(frame, 1) # Flip frame horizontally

    def release_cam(self) -> None:
        """ Releases control of a camera object. """
        self._cam.release()

    def close(self) -> None:
        """ Finishes with the camera controller """
        self.release_cam()


# Threads
def display_video_t(controller: CameraControl):
    """ Thread to display a video feed. 
    
    Params:
        controller (CameraControl): The camera controller to receive video from.
    """
    controller.create_background()
    recog = Recogniser()

    while True:
        img = controller.read_cam()
        
        # Show annotated image
        roi = controller.get_roi()
        add_roi(img, roi)
        show_image_windowed(img)

        # Make guess
        hand = controller.get_hand_segment()
        if hand:
            frame, contour = hand
            frame = process_model_image(frame)

            print(recog.predict_letter(frame))