# Electoral Roll Extractor

> Extract, process, and structure voter information from electoral roll PDFs with high accuracy.

This tool automatically extracts voter information from scanned electoral roll PDFs and converts it into structured data formats (CSV/Excel) for easy analysis and use.

### System Workflow

```mermaid
graph TB
    A[Electoral Roll PDF] -->|PDF to Images| B[Image Preprocessing]
    B -->|Enhanced Images| C[Box Detection]
    C -->|Voter Boxes| D[Text Extraction & OCR]
    D -->|Raw Text Data| E[Data Cleaning & Structuring]
    E -->|Processed Data| F[CSV/Excel Export]
    
    style A fill:#f9d5e5,stroke:#333,stroke-width:2px
    style B fill:#eeeeee,stroke:#333,stroke-width:2px
    style C fill:#d0e8f2,stroke:#333,stroke-width:2px
    style D fill:#d5f5e3,stroke:#333,stroke-width:2px
    style E fill:#fcf3cf,stroke:#333,stroke-width:2px
    style F fill:#fadbd8,stroke:#333,stroke-width:2px
```

## Key Features

- **Automated Data Extraction** - Extract voter details from PDF electoral rolls
- **Image Enhancement** - Pre-processing for improved OCR accuracy  
- **Watermark Removal** - Clean scanned documents automatically
- **Structured Output** - Organized data in CSV/Excel format
- **Easy Configuration** - Customizable for different electoral roll formats

## Technology Stack

```mermaid
flowchart LR
    A[Electoral Roll Extractor] --> B[Image Processing]
    A --> C[OCR Engine]
    A --> D[Data Processing]
    A --> E[I/O Handling]
    
    B --> B1[OpenCV • NumPy • Pillow]
    C --> C1[Tesseract • PyTesseract]
    D --> D1[Pandas • RegEx]
    E --> E1[PDF2Image • Poppler]
    
    style A fill:#f5b041,stroke:#333,stroke-width:2px
    style B fill:#82e0aa,stroke:#333,stroke-width:1px
    style C fill:#85c1e9,stroke:#333,stroke-width:1px
    style D fill:#bb8fce,stroke:#333,stroke-width:1px
    style E fill:#f7dc6f,stroke:#333,stroke-width:1px
```

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

## 🔍 How It Works

```mermaid
flowchart TD
    subgraph PDF_Processing
        A[Load PDF] --> B[Convert to Images]
    end
    
    subgraph Image_Enhancement
        B --> C[Convert to Grayscale]
        C --> D[Apply Denoising]
        D --> E[Apply Thresholding]
    end
    
    subgraph Box_Detection
        E --> F[Find Contours]
        F --> G[Filter by Size]
        G --> H[Extract Box Regions]
    end
    
    subgraph Watermark_Removal
        H --> I[Create Binary Mask]
        I --> J[Inpaint Image]
    end
    
    subgraph Text_Extraction
        J --> K[Extract Number Region]
        J --> L[Extract EPIC Number]
        J --> M[Extract Voter Info]
    end
    
    subgraph Data_Processing
        K --> N[Clean & Format Data]
        L --> N
        M --> N
        N --> O[Structure as DataFrame]
        O --> P[Export to CSV/Excel]
    end
    
    style A fill:#ffd6a5,stroke:#333,stroke-width:1px
    style B fill:#fdffb6,stroke:#333,stroke-width:1px
    style C fill:#caffbf,stroke:#333,stroke-width:1px
    style D fill:#9bf6ff,stroke:#333,stroke-width:1px
    style E fill:#bdb2ff,stroke:#333,stroke-width:1px
    style F fill:#ffc6ff,stroke:#333,stroke-width:1px
    style G fill:#ffd6a5,stroke:#333,stroke-width:1px
    style H fill:#fdffb6,stroke:#333,stroke-width:1px
    style I fill:#caffbf,stroke:#333,stroke-width:1px
    style J fill:#9bf6ff,stroke:#333,stroke-width:1px
    style K fill:#bdb2ff,stroke:#333,stroke-width:1px
    style L fill:#ffc6ff,stroke:#333,stroke-width:1px
    style M fill:#ffd6a5,stroke:#333,stroke-width:1px
    style N fill:#fdffb6,stroke:#333,stroke-width:1px
    style O fill:#caffbf,stroke:#333,stroke-width:1px
    style P fill:#9bf6ff,stroke:#333,stroke-width:1px
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
