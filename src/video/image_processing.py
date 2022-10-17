from typing import Optional, Tuple

import numpy as np
import cv2

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


def get_largest_contour_segment(img: np.ndarray) -> np.ndarray:
    """ Masks an image so that it only contains pixels within the largest 
    contour region.
    
    Params:
        img (ndarray): The image to apply the mask to.

    Returns:
        (ndarray) the filtered image.
    """
    # Find largest contour
    contours, heirarchy = cv2.findContours(
        img, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)
    biggest_contour = max(contours, key=lambda item: cv2.contourArea(item))
    
    # Create mask of contour
    mask = np.zeros_like(img)
    cv2.drawContours(mask, [biggest_contour], -1, (255, 255, 255), cv2.FILLED)
    
    # Remove other bits
    res = cv2.bitwise_and(img, img, mask=mask)
    return res

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
    # Remove pixels that are not in the largest blob
    filtered = get_largest_contour_segment(scaled)
    # Convert grayscale to RGB
    coloured = cv2.cvtColor(filtered, cv2.COLOR_GRAY2RGB)
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