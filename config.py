"""
Configuration settings for the Electoral Roll Extractor.

This module contains all the configuration parameters used by the application,
including file paths, OCR settings, and image processing parameters.
"""
import os
from pathlib import Path

# Base directories
BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / "data"
INPUT_DIR = DATA_DIR / "input"
OUTPUT_DIR = DATA_DIR / "output"
DEBUG_DIR = DATA_DIR / "debug"

# Create directories if they don't exist
for directory in [INPUT_DIR, OUTPUT_DIR, DEBUG_DIR]:
    os.makedirs(directory, exist_ok=True)

# File paths
DEFAULT_PDF_PATH = INPUT_DIR / "electoral_roll_data.pdf"
CSV_OUTPUT_PATH = OUTPUT_DIR / "extracted_data.csv"
EXCEL_OUTPUT_PATH = OUTPUT_DIR / "processed_data.xlsx"

# OCR Configuration
TESSERACT_CMD = r'C:\Program Files\Tesseract-OCR\tesseract.exe'  # Adjust for your system
POPPLER_PATH = r'C:\Program Files (x86)\poppler-0.68.0\bin'  # Adjust for your system

# Image processing parameters
IMAGE_PARAMS = {
    # Denoising parameters
    'denoising_strength': 10,
    'template_window_size': 7,
    'search_window_size': 21,
    
    # Contour detection parameters
    'contour_area_threshold': 100,
    'max_contours': 30,
    
    # Text extraction parameters
    'contrast_enhancement': 2.0,
    'number_width': 30,
    
    # Debug settings
    'save_debug_images': True,
    'debug_image_interval': 5  # Save debug image every nth box
}

# Data columns
INPUT_COLUMNS = ["number", "top_right_text", "line1", "line2", "line3", "line4"]
OUTPUT_COLUMNS = [
    "Part S.No", 
    "Voter Full Name", 
    "Relative's Name",
    "Relation Type", 
    "Age", 
    "Gender", 
    "House No", 
    "EPIC No"
]

# Logging configuration
LOG_FILE = DEBUG_DIR / "electoral_roll_extractor.log"
LOG_LEVEL = "INFO"
LOG_FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
