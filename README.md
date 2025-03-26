# Electoral Roll Extractor

> Extract, process, and structure voter information from electoral roll PDFs with high accuracy.

This tool automatically extracts voter information from scanned electoral roll PDFs and converts it into structured data formats (CSV/Excel) for easy analysis and use.

## System Workflow and Technology Stack

```mermaid
flowchart TD
    A([<b>Electoral Roll PDF</b>]) --> B
    
    subgraph B[<b>Image Processing</b>]
      B1[<b>PDF to Images<br>Grayscale Conversion<br>Noise Reduction<br>Binary Thresholding</b>]
      B2[<b>Technologies:<br>PDF2Image, Poppler<br>OpenCV, Pillow</b>]
      B1 --- B2
    end
    
    B --> C
    
    subgraph C[<b>Box Detection</b>]
      C1[<b>Contour Detection<br>Region Extraction<br>Watermark Removal</b>]
      C2[<b>Technologies:<br>OpenCV, NumPy</b>]
      C1 --- C2
    end
    
    C --> D
    
    subgraph D[<b>Text Extraction</b>]
      D1[<b>Region Identification<br>OCR Processing<br>Text Collection</b>]
      D2[<b>Technologies:<br>Tesseract</b>]
      D1 --- D2
    end
    
    D --> E
    
    subgraph E[<b>Data Processing</b>]
      E1[<b>Text Cleaning<br>Field Extraction<br>Data Structuring</b>]
      E2[<b>Technologies:<br>Pandas, RegEx</b>]
      E1 --- E2
    end
    
    E --> F([<b>Structured Output</b>])
    
    style A fill:#f5b041,stroke:#333,stroke-width:2px
    style F fill:#f5b041,stroke:#333,stroke-width:2px
    style B fill:#82e0aa,stroke:#333,stroke-width:1px
    style C fill:#85c1e9,stroke:#333,stroke-width:1px
    style D fill:#bb8fce,stroke:#333,stroke-width:1px
    style E fill:#f7dc6f,stroke:#333,stroke-width:1px
    
    classDef subboxes fill:white,stroke:#ddd,stroke-width:1px
    class B1,B2,C1,C2,D1,D2,E1,E2 subboxes
```

## Key Features

- **Automated Data Extraction** - Extract voter details from PDF electoral rolls
- **Image Enhancement** - Pre-processing for improved OCR accuracy  
- **Watermark Removal** - Clean scanned documents automatically
- **Structured Output** - Organized data in CSV/Excel format
- **Easy Configuration** - Customizable for different electoral roll formats


## 📋 Requirements

- Python 3.7+
- Tesseract OCR
- Poppler utilities
- `opencv`

### Installation

```bash
# Clone the repository
git clone https://github.com/yourusername/electoral-roll-extractor.git
cd electoral-roll-extractor

# Install dependencies
pip install -r requirements.txt

# Install Tesseract OCR and Poppler (system-specific)
# Windows: Download from respective websites
# Linux: sudo apt install tesseract-ocr poppler-utils
# macOS: brew install tesseract poppler
```

### Configuration

Update paths in `config.py` to match your environment:

```python
# Adjust these paths according to your system
TESSERACT_CMD = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
POPPLER_PATH = r'path\to\poppler\bin'
```


### Project Structure

```
electoral-roll-extractor/
├── config.py                  # Configuration settings
├── main.py                    # Main entry point
├── requirements.txt           # Dependencies
├── extractor/
│   ├── __init__.py
│   ├── image_processor.py     # Image processing functions
│   ├── text_extractor.py      # OCR and text extraction
│   ├── data_processor.py      # Data processing and formatting
│   └── utils.py               # Utility functions
└── data/                      # Data directory for input/output
    ├── input/                 # Input PDF files
    ├── output/                # Processed data output
    └── debug/                 # Debug images and logs
```
