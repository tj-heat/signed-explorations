from turtle import width
from typing import Optional, Tuple

import cv2
import numpy as np

from src.video.image_processing import Recogniser

CAPTURING = True # Temp const for feature enabling
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
    """ Crops an image to the ROI
    
    Params:
        img (np.ndarray): The image to crop.
        roi ((int, int), (int, int)): Two tuples indicating the TL and BR 
            corners of the image ROI.

    Returns:
        (np.ndarray) The cropped image.
    """
    (left, top), (right, bottom) = roi
    return img[top:bottom, left:right]

def get_image_gray(img: np.ndarray) -> np.ndarray:
    """ Convert an image in BGR space to grayscale.
    
    Params:
        img (np.ndarray): The BGR colourspace image to convert.
    
    Returns:
        (np.ndarray) A grayscale image.
    """
    return cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

def get_image_blur(img: np.ndarray) -> np.ndarray:
    """ Applies a strong gaussian blur to an image. """
    return cv2.GaussianBlur(img, (9, 9), 0)

def get_image_diff(img: np.ndarray, ref: np.ndarray) -> np.ndarray:
    """ Finds the absolute difference between two images. 
    
    Raises:
        (ValueError) If the two images do not match in shape or size.
    """
    if img.shape != ref.shape:
        raise ValueError("Provided images do not match in shape/size")

    return cv2.absdiff(ref.astype("uint8"), img)

def get_image_binary(img: np.ndarray, thresh: int):
    """ Converts a grayscale image to binary.
    
    Params:
        img (np.ndarray): The grayscale image to convert.
        thresh (int): The threshold to use when converting to binary.
    
    Returns:
        (np.ndarray) A binary image.
    """
    _, binary = cv2.threshold(img, thresh, 255, cv2.THRESH_BINARY)
    return binary

def preprocess_image(img: np.ndarray) -> np.ndarray:
    """ Converts an image into a grayscale and blurred image. """
    gray = get_image_gray(img)
    blur = get_image_blur(gray)
    return blur

def crop_and_preprocess(
    img: np.ndarray, 
    roi: Tuple[Tuple[int, int], Tuple[int, int]]
) -> np.ndarray:
    """ Convenience function for cropping and preprocessing. """
    return preprocess_image(get_image_roi(img, roi))

def process_hand_image(img: np.ndarray, ref: np.ndarray, thresh: int):
    """ Processes a grayscale, blurred image into binary image of a hand, based 
    on differences with a reference image. 
    
    Precondition:
        The image is grayscale and has been blurred.

    Params:
        img (np.ndarray): The grayscale image to convert.
        ref (np.ndarray): The reference image to difference with.
        thresh (int): The threshold to use when converting to binary.
    
    Returns:
        (np.ndarray) A binary image containing the difference with ref.
    """
    diff = get_image_diff(img, ref)
    binary = get_image_binary(diff, thresh)
    return binary

def process_model_image(img: np.ndarray):
    """ Processes an image to prepare it for the recognition model. The model 
    expects images to be 64x64, RGB, and with 3 colour channels. The provided 
    image should be a binary image of a hand shape.
    
    Precondition:
        The provided image is a binarised hand gesture capture.

    Params:
        img (np.ndarray): The binary image to process for the model.

    Returns:
        (np.ndarray): An image in the format the recognition model expects.
    """
    # Make 64x64
    scaled = cv2.resize(img, (64, 64))
    # Convrt grayscale to RGB
    coloured = cv2.cvtColor(scaled, cv2.COLOR_GRAY2RGB)
    # Turn into array of 1x64x64 with three colour channels
    shaped = np.reshape(coloured, (1, coloured.shape[0], coloured.shape[1], 3))
    return shaped

def get_hand_segment(
    background: np.ndarray, 
    img: np.ndarray,
    roi: Tuple[Tuple[int, int], Tuple[int, int]],
    thresh: int = 25
) -> Optional[Tuple[np.ndarray]]:
    """ Attempt to get the segmentation information for any detected hands in 
    an image. 
    
    Params:
        background (np.ndarray): The accumulated average background from a 
            camera controller.
        img (np.ndarray): The unedited and uncropped image to look for a hand
            segment in.
        thresh (int): The threshold used to binarise the image. Defaults to 25.

    Returns:
        (Tuple(np.ndarray)) If a hand segment is detected, returns the binary 
            image containing the hand, as well as the longest contour found in 
            the image.
    """
    crop = get_image_roi(img, roi)
    processed = preprocess_image(crop)
    binary = process_hand_image(processed, background, thresh)
    
    contours, _ = cv2.findContours(
        binary, 
        cv2.RETR_EXTERNAL, 
        cv2.CHAIN_APPROX_SIMPLE
    )

    if len(contours):
        largest_contour = max(contours, key=cv2.contourArea)
        return (binary, largest_contour)

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
def display_video_t(controller: CameraControl):
    """ Thread to display a video feed. 
    
    Params:
        controller (CameraControl): The camera controller to receive video from.
    """
    recog = Recogniser()
    controller.create_background()

    while True:
        bg = controller.get_background()
        img = controller.read_cam()
        roi = controller.get_roi()
        
        # Show annotated image
        add_roi(img, roi)
        show_image_windowed(img)

        # Make guess
        hand = get_hand_segment(bg, img, roi)
        if hand:
            frame, contour = hand
            frame = process_model_image(frame)

            print(recog.predict_letter(frame))