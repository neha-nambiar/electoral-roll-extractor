"""
Image processing utilities for electoral roll extraction.

This file contains functions for processing images, including preprocessing,
watermark removal, and detection of regions of interest.
"""
import cv2
import numpy as np
import logging
from typing import List, Tuple, Optional

from config import IMAGE_PARAMS

# Set up logger
logger = logging.getLogger(__name__)

def preprocess_image(img: np.ndarray) -> np.ndarray:
    """
    Preprocess the input image for OCR by converting it to grayscale, denoising it, 
    and applying thresholding to create a binary image.

    Args:
        img: The input image in BGR format.

    Returns:
        The preprocessed binary image after thresholding.
    """
    try:
        # Convert to grayscale
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        
        # Apply denoising
        denoised = cv2.fastNlMeansDenoising(
            gray, 
            None, 
            IMAGE_PARAMS['denoising_strength'],
            IMAGE_PARAMS['template_window_size'],
            IMAGE_PARAMS['search_window_size']
        )
        
        # Apply thresholding
        thresh = cv2.threshold(
            denoised, 
            0, 
            255, 
            cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU
        )[1]
        
        return thresh
    except Exception as e:
        logger.error(f"Error preprocessing image: {e}")
        raise


def remove_watermark(img: np.ndarray) -> np.ndarray:
    """
    Remove the watermark from the input image using morphological operations 
    and inpainting techniques.

    Args:
        img: The input image in BGR format.

    Returns:
        The image with the watermark removed.
    """
    try:
        # Convert to grayscale
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        
        # Create a binary mask of the watermark
        _, thresh = cv2.threshold(gray, 180, 255, cv2.THRESH_BINARY_INV)
        
        # Create a kernel for morphological operations
        kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3))
        
        # Perform dilation to connect watermark components
        dilated = cv2.dilate(thresh, kernel, iterations=2)
        
        # Find contours of the watermark
        contours, _ = cv2.findContours(
            dilated, 
            cv2.RETR_EXTERNAL, 
            cv2.CHAIN_APPROX_SIMPLE
        )
        
        # Create a mask to store the watermark area
        mask = np.zeros(gray.shape, np.uint8)
        
        # Draw the contours on the mask
        for contour in contours:
            if cv2.contourArea(contour) > IMAGE_PARAMS['contour_area_threshold']:
                cv2.drawContours(mask, [contour], 0, (255, 255, 255), -1)
        
        # Inpaint the watermark area
        result = cv2.inpaint(img, mask, 3, cv2.INPAINT_TELEA)
        
        return result
    except Exception as e:
        logger.error(f"Error removing watermark: {e}")
        raise


def find_boxes(img: np.ndarray) -> List[Tuple[int, int, int, int]]:
    """
    Find the largest rectangular boxes (contours) in the preprocessed image, 
    which represent regions containing important information.

    Args:
        img: The input preprocessed binary image.

    Returns:
        A list of bounding rectangles for the largest contours in the image.
        Each rectangle is represented as (x, y, width, height).
    """
    try:
        # Find all contours
        contours, _ = cv2.findContours(
            img, 
            cv2.RETR_EXTERNAL, 
            cv2.CHAIN_APPROX_SIMPLE
        )
        
        # Sort contours by area (largest first)
        contours = sorted(contours, key=cv2.contourArea, reverse=True)
        
        # Get the N largest contours
        largest_contours = contours[:IMAGE_PARAMS['max_contours']]
        
        # Convert contours to bounding rectangles
        boxes = [cv2.boundingRect(contour) for contour in largest_contours]
        
        return boxes
    except Exception as e:
        logger.error(f"Error finding boxes: {e}")
        raise


def find_inner_boxes(roi: np.ndarray) -> List[Tuple[int, int, int, int]]:
    """
    Find inner boxes within a region of interest (ROI) of an image, specifically in 
    the top-left corner, which typically contains a smaller box of interest.

    Args:
        roi: The region of interest (ROI) of the image.

    Returns:
        A list of bounding rectangles for the inner boxes found in the top-left region.
        Each rectangle is represented as (x, y, width, height).
    """
    try:
        # Get dimensions of the ROI
        h, w = roi.shape
        
        # Extract the top-left region
        top_left = roi[0:h//3, 0:w//3]
        
        # Find contours in the top-left region
        contours_tl, _ = cv2.findContours(
            top_left, 
            cv2.RETR_EXTERNAL, 
            cv2.CHAIN_APPROX_SIMPLE
        )
        
        # If contours are found, return the largest one
        if contours_tl:
            box_tl = cv2.boundingRect(max(contours_tl, key=cv2.contourArea))
            return [box_tl]
            
        return []
    except Exception as e:
        logger.error(f"Error finding inner boxes: {e}")
        raise


def create_debug_image(
    img: np.ndarray,
    boxes: List[Tuple[int, int, int, int]],
    current_box_idx: Optional[int] = None,
    inner_box: Optional[Tuple[int, int, int, int]] = None
) -> np.ndarray:
    """
    Create a debug image showing the detected boxes.

    Args:
        img: The original image.
        boxes: List of detected boxes.
        current_box_idx: Index of the current box being processed (optional).
        inner_box: Inner box coordinates relative to the current box (optional).

    Returns:
        A new image with visualized boxes.
    """
    try:
        # Create a copy of the image
        debug_img = img.copy()
        
        # Draw all outer boxes
        for i, (x, y, w, h) in enumerate(boxes):
            # Use green for regular boxes, red for the current box
            color = (0, 0, 255) if i == current_box_idx else (0, 255, 0)
            thickness = 2 if i == current_box_idx else 1
            
            # Draw rectangle
            cv2.rectangle(debug_img, (x, y), (x+w, y+h), color, thickness)
            
            # Add box number
            cv2.putText(
                debug_img,
                f"{i+1}",
                (x+5, y+20),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.6,
                color,
                1
            )
        
        # Draw inner box if provided
        if current_box_idx is not None and inner_box is not None:
            # Get coordinates of the current outer box
            x, y, _, _ = boxes[current_box_idx]
            
            # Get coordinates of the inner box
            ix, iy, iw, ih = inner_box
            
            # Draw the inner box (blue)
            cv2.rectangle(
                debug_img,
                (x+ix, y+iy),
                (x+ix+iw, y+iy+ih),
                (255, 0, 0),
                2
            )
        
        return debug_img
    except Exception as e:
        logger.error(f"Error creating debug image: {e}")
        return img  # Return original image on error
