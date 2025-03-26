"""
Text extraction utilities for electoral roll extraction.

This file contains functions for extracting text from processed images using OCR.
"""
import cv2
import numpy as np
import pytesseract
from PIL import Image, ImageEnhance
import logging
from typing import Dict, Any, Tuple

from config import IMAGE_PARAMS
from extractor.image_processor import remove_watermark

# Set up logger
logger = logging.getLogger(__name__)

def extract_number(
    img: np.ndarray, 
    x: int, 
    y: int, 
    w: int, 
    h: int
) -> str:
    """
    Extract a number from a specific region in the image, enhancing contrast and 
    using OCR to recognize the digits.

    Args:
        img: The input image in BGR format.
        x: The x-coordinate of the top-left corner of the region.
        y: The y-coordinate of the top-left corner of the region.
        w: The width of the region.
        h: The height of the region.

    Returns:
        The extracted number as a string.
    """
    try:
        # Extract the region of interest
        roi = img[y:y+h, x:x+w]
        
        # Convert to PIL image for enhancement
        pil_img = Image.fromarray(roi)
        
        # Increase contrast
        enhancer = ImageEnhance.Contrast(pil_img)
        pil_img = enhancer.enhance(IMAGE_PARAMS['contrast_enhancement'])
        
        # Convert back to numpy array
        roi = np.array(pil_img)
        
        # Convert to grayscale
        gray_roi = cv2.cvtColor(roi, cv2.COLOR_BGR2GRAY)
        
        # Create binary image
        _, binary = cv2.threshold(gray_roi, 200, 255, cv2.THRESH_BINARY_INV)
        
        # Find non-white columns
        col_sums = np.sum(binary, axis=0)
        
        # Check if there are any non-white pixels
        if np.max(col_sums) > 0:
            # Find the rightmost non-white column
            rightmost_col = np.max(np.where(col_sums > 0))
            
            # Extract a small region around the rightmost number
            number_width = IMAGE_PARAMS['number_width']
            number_roi = roi[0:h, max(0, rightmost_col-number_width):rightmost_col+5]
            
            # Perform OCR with specific configuration for digits
            number = pytesseract.image_to_string(
                number_roi, 
                config='--psm 10 --oem 3 -c tessedit_char_whitelist=0123456789'
            ).strip()
            
            return number
        
        return ""
    except Exception as e:
        logger.error(f"Error extracting number: {e}")
        return ""


def extract_text(
    img: np.ndarray, 
    x: int, 
    y: int, 
    w: int, 
    h: int
) -> str:
    """
    Extract text from a specific region in the image using OCR.

    Args:
        img: The input image in BGR format.
        x: The x-coordinate of the top-left corner of the region.
        y: The y-coordinate of the top-left corner of the region.
        w: The width of the region.
        h: The height of the region.

    Returns:
        The extracted text as a string.
    """
    try:
        # Extract the region of interest
        roi = img[y:y+h, x:x+w]
        
        # Perform OCR with page segmentation mode 6 (assume a single uniform block of text)
        text = pytesseract.image_to_string(roi, config='--psm 6').strip()
        
        return text
    except Exception as e:
        logger.error(f"Error extracting text: {e}")
        return ""


def process_voter_box(
    img: np.ndarray,
    box: Tuple[int, int, int, int],
    inner_box: Tuple[int, int, int, int]
) -> Dict[str, Any]:
    """
    Process a voter information box and extract all relevant text fields.

    Args:
        img: The original image in BGR format.
        box: The coordinates of the voter box (x, y, width, height).
        inner_box: The coordinates of the inner box containing the voter number.

    Returns:
        A dictionary containing the extracted information.
    """
    try:
        # Extract coordinates
        x, y, w, h = box
        ix, iy, iw, ih = inner_box
        
        # Extract the box image
        box_img = img[y:y+h, x:x+w]
        
        # Remove watermark
        clean_img = remove_watermark(box_img)
        
        # Extract voter number from inner box
        number = extract_number(clean_img, ix, iy, iw, ih)
        
        # Extract top right text (EPIC number)
        top_right_text = extract_text(clean_img, iw+10, 0, w-iw-10, ih)
        
        # Define region for the main text block
        text_x = 5
        text_y = iy + ih + 5
        text_w = int(w * 2/3)
        text_h = h - text_y - 5
        
        # Extract main text
        text = extract_text(clean_img, text_x, text_y, text_w, text_h)
        
        # Split into lines
        lines = text.split('\n')
        lines = [line.strip() for line in lines if line.strip()]
        
        # Ensure we have exactly 4 lines
        while len(lines) < 4:
            lines.append('')
        
        # Take only the first 4 lines
        lines = lines[:4]
        
        # Return structured data
        return {
            'number': number,
            'top_right_text': top_right_text,
            'line1': lines[0],
            'line2': lines[1],
            'line3': lines[2],
            'line4': lines[3]
        }
    except Exception as e:
        logger.error(f"Error processing voter box: {e}")
        return {
            'number': '',
            'top_right_text': '',
            'line1': '',
            'line2': '',
            'line3': '',
            'line4': ''
        }
