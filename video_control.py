from typing import Optional

import numpy as np
import cv2

CAPTURING = False # Temp const for feature enabling
DEFAULT_WINDOW = "Camera Capture"

# Functions
def show_image_windowed(img: np.ndarray, window: str = DEFAULT_WINDOW) -> None:
    """ Display an image in a window separate to the game window. """
    cv2.imshow(window, img)
    cv2.waitKey(1)


# Classes
class CameraControl():

    def __init__(self) -> None:
        self._cam = self.get_cam()
    
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
        show_image_windowed(controller.read_cam())