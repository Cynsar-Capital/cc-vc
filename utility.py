import pandas as pd

def extract_data(filename):
    """
    Extracts data from a given file (CSV or Excel).
    
    Parameters:
    - filename (str): Name of the file along with its extension.

    Returns:
    - DataFrame: Extracted data in the form of a pandas DataFrame.
    """
    
    # Check the file extension to determine the file type
    file_extension = filename.split('.')[-1]
    
    if file_extension == "csv":
        data = pd.read_csv(filename)
    elif file_extension in ["xls", "xlsx"]:
        data = pd.read_excel(filename)
    else:
        raise ValueError("Unsupported file format. Please provide a CSV or Excel file.")
        
    return data


def table_to_string(table):
    return "\n".join(["\t".join(map(str, row)) for row in table])


def reduce_duplicates(s):
    if not s:
        return s

    result = [s[0]]  # Start with the first character

    for i in range(1, len(s)):
        # If current character is not the same as the previous one, add it to the result
        if s[i] != s[i-1]:
            result.append(s[i])

    return ''.join(result)

def remove_consecutive_duplicates(text):
    cleaned_text = []
    prev_char = None
    for char in text:
        if char != prev_char:
            cleaned_text.append(char)
        prev_char = char
    return ''.join(cleaned_text)




