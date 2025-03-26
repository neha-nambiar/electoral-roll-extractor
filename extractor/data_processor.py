"""
Data processing utilities for electoral roll extraction.

This file contains functions for cleaning, transforming, and formatting
the extracted raw data into structured output.
"""
import pandas as pd
import re
import logging
from typing import Tuple, Optional, Any, List

# Set up logger
logger = logging.getLogger(__name__)

def extract_and_format_name(text: str) -> str:
    """
    Extract and format a name from the given text.

    This function removes any non-alphabetic characters (except spaces) from the input text,
    trims extra spaces, and capitalizes the first letter of each word. The function assumes
    that the name starts after the first word in the input string.

    Args:
        text: The input text containing the name.

    Returns:
        The formatted name, with the first letter of each word capitalized. Returns an empty
        string if the name could not be extracted.
    """
    try:
        if not isinstance(text, str):
            return ""
            
        # Remove any non-alphabetic characters (except space) and extra spaces
        cleaned = re.sub(r'[^a-zA-Z\s]', '', text)
        cleaned = re.sub(r'\s+', ' ', cleaned).strip()
        
        # Split the string and take all words after the first one (assumed to be "Name")
        parts = cleaned.split(' ')
        if len(parts) > 1:
            name = ' '.join(parts[1:])
            
            # Capitalize the first letter of each word
            name = ' '.join(word.capitalize() for word in name.split())
            
            return name
        
        return ""
    except Exception as e:
        logger.error(f"Error extracting name: {e}")
        return ""
    
    
def extract_name_and_relation(text: str) -> Tuple[str, str]:
    """
    Extract a name and determine the relationship type from the given text.

    This function removes non-alphabetic characters (except spaces) and extra spaces from the
    input text, extracts the name after the keywords "name" or "others," and determines the
    relationship type based on keywords such as "father," "husband," or "others." The name is
    formatted with the first letter of each word capitalized.

    Args:
        text: The input text containing the name and relationship information.

    Returns:
        A tuple containing:
            - name (str): The formatted name with the first letter of each word capitalized.
            - relation (str): A short code representing the relationship type:
              "FTHR" for father, "HSBN" for husband, "OTHR" for others, or an empty string if no
              relationship type is detected.
    """
    try:
        if not isinstance(text, str):
            return "", ""
            
        # Remove any non-alphabetic characters (except space) and extra spaces
        cleaned = re.sub(r'[^a-zA-Z\s]', ' ', text)
        cleaned = re.sub(r'\s+', ' ', cleaned).strip().lower()
        
        # Extract name
        name_match = re.search(r'(?:name|others)\s*(.*)', cleaned)
        name = name_match.group(1).strip() if name_match else ''
        
        # Format name
        name = ' '.join(word.capitalize() for word in name.split())
        
        # Determine relation type
        if "father" in cleaned:
            relation = "FTHR"
        elif "husband" in cleaned:
            relation = "HSBN"
        elif "others" in cleaned:
            relation = "OTHR"
        else:
            relation = ""
        
        return name, relation
    except Exception as e:
        logger.error(f"Error extracting name and relation: {e}")
        return "", ""


def extract_house_number(text: str) -> str:
    """
    Extract the house number from the given text.

    This function removes non-alphanumeric characters (except spaces and hyphens) and extra spaces
    from the input text, and attempts to extract the house number following the phrase "house number."
    If the extracted entry is empty or consists only of a hyphen, it is returned as is.

    Args:
        text: The input text containing the house number information.

    Returns:
        The extracted house number, with leading and trailing spaces or hyphens removed. Returns
        an empty string if no house number is detected.
    """
    try:
        if not isinstance(text, str):
            return ""
            
        # Remove any non-alphanumeric characters (except space and hyphen) and extra spaces
        cleaned = re.sub(r'[^a-zA-Z0-9\s-]', ' ', str(text))
        cleaned = re.sub(r'\s+', ' ', cleaned).strip().lower()
        
        # Try to find the entry after "house number" and any characters
        match = re.search(r'house\s*number.*?[:\s](.*)', cleaned)
        
        if match:
            entry = match.group(1).strip()
            # If entry is empty or just a hyphen, return it as is
            if entry in ['', '-']:
                return entry
            # Otherwise, remove any leading/trailing spaces or hyphens
            return entry.strip(' -')
        
        return ""
    except Exception as e:
        logger.error(f"Error extracting house number: {e}")
        return ""
    
    
def clean_number(value: Any) -> Optional[int]:
    """
    Clean and convert a number from the given value.

    This function converts the input value to a string, removes everything after the first decimal point,
    and removes any non-digit characters. The cleaned value is then converted to an integer. If the cleaned
    value does not contain any digits, the function returns `pd.NA`.

    Args:
        value: The input value containing the number (can be any data type).

    Returns:
        The cleaned and converted integer value, or `pd.NA` if the value does not contain
        any digits.
    """
    try:
        if pd.isna(value):  # Check if the value is NaN
            return pd.NA
        
        # Convert the value to a string
        value_str = str(value)
        
        # Stop at the decimal point (remove everything after the first decimal)
        before_decimal = value_str.split('.')[0]
        
        # Remove any non-digit characters
        cleaned = re.sub(r'\D', '', before_decimal)
        
        # If we have digits, convert to integer
        if cleaned:
            return int(cleaned)
        
        return pd.NA
    except Exception as e:
        logger.error(f"Error cleaning number: {e}")
        return pd.NA
    
    
def extract_age(text: str) -> Optional[int]:
    """
    Extract age from the given text.

    This function searches the input text for a pattern that matches "Age" followed by a separator (e.g., 
    ":", "!", "l", "+") and a numeric value, and returns the extracted age as an integer.

    Args:
        text: The input text containing the age information.

    Returns:
        The extracted age as an integer, or `None` if no age is found.
    """
    try:
        if not isinstance(text, str):
            return None
            
        match = re.search(r'Ag[ee]\s*[:!l+]\s*(\d+)', text, re.IGNORECASE)
        return int(match.group(1)) if match else None
    except Exception as e:
        logger.error(f"Error extracting age: {e}")
        return None


def extract_gender(text: str) -> Optional[str]:
    """
    Extract gender from the given text.

    This function searches the input text for a pattern that matches "Gender" followed by a separator (e.g., 
    ":", "!", "l", "+") and a gender-related word (e.g., "Male", "Female"). It returns 'M' for male and 'F' 
    for female. If the direct match fails, a more lenient approach is used to search for "ma" or "fe" 
    patterns to determine the gender.

    Args:
        text: The input text containing the gender information.

    Returns:
        The gender as 'M' (male) or 'F' (female), or `None` if no gender is detected.
    """
    try:
        if not isinstance(text, str):
            return None
            
        match = re.search(r'Gen[de]r\s*[:!l+]\s*(\w+)', text, re.IGNORECASE)
        if match:
            gender = match.group(1).lower()
            if re.search(r'ma', gender):
                return 'M'
            elif re.search(r'fe', gender):
                return 'F'

        # If the above doesn't work, try a more lenient approach
        if re.search(r'\bma', text.lower()):
            return 'M'
        elif re.search(r'\bfe', text.lower()):
            return 'F'

        return None
    except Exception as e:
        logger.error(f"Error extracting gender: {e}")
        return None


def process_raw_data(df: pd.DataFrame, required_columns: List[str]) -> pd.DataFrame:
    """
    Process the raw extracted data to create a structured DataFrame.
    
    Args:
        df: The input DataFrame containing raw extracted data.
        required_columns: List of columns that must not be all null.
        
    Returns:
        A processed DataFrame with cleaned and structured data.
    """
    try:
        logger.info("Processing raw data...")
        
        # Drop rows where all required columns are NaN
        filtered_df = df.dropna(subset=required_columns, how='all').reset_index(drop=True)
        logger.info(f"Filtered from {len(df)} to {len(filtered_df)} valid entries")
        
        # Extract structured data
        processed_df = pd.DataFrame()
        
        # Extract EPIC No from top_right_text
        processed_df['EPIC No'] = filtered_df['top_right_text'].str.replace(r'[^A-Z0-9]', '', regex=True)
        
        # Extract and format voter name
        processed_df['Voter Full Name'] = filtered_df['line1'].apply(extract_and_format_name)
        
        # Extract relative's name and relation type
        processed_df['Relative\'s Name'], processed_df['Relation Type'] = zip(
            *filtered_df['line2'].apply(extract_name_and_relation)
        )
        
        # Extract house number
        processed_df['House No'] = filtered_df['line3'].apply(extract_house_number)
        
        # Clean and convert part number
        processed_df['Part S.No'] = filtered_df['number'].apply(clean_number)
        
        # Extract age
        processed_df['Age'] = filtered_df['line4'].apply(extract_age)
        
        # Extract gender
        processed_df['Gender'] = filtered_df['line4'].apply(extract_gender)
        
        # Sort by part number
        processed_df = processed_df.sort_values(by='Part S.No', ascending=True)
        
        # Add metadata columns if needed
        if 'page' in filtered_df.columns:
            processed_df['Page'] = filtered_df['page']
            
        if 'box' in filtered_df.columns:
            processed_df['Box'] = filtered_df['box']
        
        logger.info(f"Processed data contains {len(processed_df)} rows")
        return processed_df
        
    except Exception as e:
        logger.error(f"Error processing raw data: {e}")
        raise
