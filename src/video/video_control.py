from turtle import width
from typing import Tuple

import cv2
import numpy as np

CAPTURING = True # Temp const for feature enabling
DEFAULT_WINDOW = "Camera Capture"

# Functions
def add_roi(
    img: np.ndarray, 
    top_left: Tuple[int, int], 
    bot_right: Tuple[int, int],
    colour: Tuple[int, int, int] = (255, 0, 255), # Magenta
    width: int = 2
) -> None:
    """ Draws the ROI to a given frame. 
    
    Params:
        img (ndarray): The frame to add the ROI to.
        top_left (Tuple): A tuple containing the x, y position of the top-left 
            ROI corner
        bot_right (Tuple): A tuple containing the x, y position of the bottom-
            right ROI corner
        colour (Tuple): The RGB values (0-255) to draw the ROI with
        width (int): The pixel width of the ROI
    """
    cv2.rectangle(img, top_left, bot_right, colour, width)

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

    def release_cam(self) -> None:
        """ Releases control of a camera object. """
        self._cam.release()

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

        return frame

    def close(self) -> None:
        """ Finishes with the camera controller """
        self.release_cam()


# Threads
def display_video_t(controller: CameraControl):
    """ Thread to display a video feed. 
    
    Params:
        controller (CameraControl): The camera controller to receive video from.
    """
    while True:
        img = controller.read_cam()
        
        # Calculate ROI
        x_mid, y_mid = [int(dim / 2) for dim in controller.get_dimensions()]
        x_offset = controller.ROI_WIDTH // 2
        y_offset = controller.ROI_HEIGHT // 2
        tl = (x_mid - x_offset, y_mid - y_offset)
        br = (x_mid + x_offset, y_mid + y_offset)
        
        # Show annotated image
        add_roi(img, tl, br)
        show_image_windowed(img)