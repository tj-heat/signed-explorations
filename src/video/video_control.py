from turtle import width
from typing import Optional, Tuple

import cv2
import numpy as np

from src.video.image_processing import add_roi, crop_and_preprocess, \
    get_hand_segment, process_model_image
from src.video.image_recognition import Recogniser

from src.util.ring_buffer import RingBuffer
from src.util.thread_control import ThreadCloser

CAPTURING = True # Temp const for feature enabling
WINDOW_DISPLAY = False
DEFAULT_WINDOW = "Camera Capture"

# Functions
def show_image_windowed(img: np.ndarray, window: str = DEFAULT_WINDOW) -> None:
    """ Display an image in a window separate to the game window. 
    Likely a temporary function.
    """
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

    def create_background(self, weight: float = 0.5) -> None:
        """ Generates an accumulated average background for differencing. 
        Background is stored internally. 
        
        Params:
            weight (float): The weight with which to calculated the accumulaated
                average.
        """
        roi = self.get_roi()

        # Initial background
        self._background = crop_and_preprocess(self.read_cam(), roi) \
            .astype("float")

        # Generate accumulated average
        for _ in range(60):
            # # At 60fps this will take one second
            frame = crop_and_preprocess(self.read_cam(), roi)
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

    def get_background(self) -> np.ndarray:
        """ (np.ndarray) Returns the background image for the controller"""
        return self._background

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
def display_video_t(
    controller: CameraControl, 
    buffer: RingBuffer, 
    closer: ThreadCloser
) -> None:
    """ Thread to display a video feed. 
    
    Params:
        controller (CameraControl): The camera controller to receive video from.
        buffer (RingBuffer): Shared memory location for image producing.
    """
    recog = Recogniser()
    controller.create_background()
    bg = controller.get_background()

    while not closer.is_killed():
        # Ensure active
        closer.wait()

        img = controller.read_cam()
        roi = controller.get_roi()
        predicted = None
        
        # Show annotated image
        add_roi(img, roi)
        show_image_windowed(img)

        hand = get_hand_segment(bg, img, roi)
        if hand:
            frame, contour = hand
            frame = process_model_image(frame)
            predicted = recog.predict_letter(frame)

        # Add image to buffer
        buffer.put((cv2.cvtColor(img, cv2.COLOR_BGR2RGB), predicted))

    # Thread should die. Begin cleanup
    #controller.release_cam() 
    # FIXME If we release here, can't restart game from menu