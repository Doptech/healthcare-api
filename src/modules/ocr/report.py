import re

def extract_diabetic_report_high_blood_pressure(text):
    # Define regular expressions to match relevant values
    glucose_pattern = r"glucose\s+(\d+(?:\.\d+)?)\s+mg/dL"
    a1c_pattern = r"A1C\s+(\d+(?:\.\d+)?)%"
    systolic_bp_pattern = r"systolic\s+blood\s+pressure\s+(\d+)\s+mmHg"
    diastolic_bp_pattern = r"diastolic\s+blood\s+pressure\s+(\d+)\s+mmHg"

    # Find matches for each pattern in the input text
    glucose_match = re.search(glucose_pattern, text, re.IGNORECASE)
    a1c_match = re.search(a1c_pattern, text, re.IGNORECASE)
    systolic_bp_match = re.search(systolic_bp_pattern, text, re.IGNORECASE)
    diastolic_bp_match = re.search(diastolic_bp_pattern, text, re.IGNORECASE)

    # Create a dictionary to store the extracted values
    extracted_values = {}

    # Add the glucose value if found
    if glucose_match:
        extracted_values["glucose"] = float(glucose_match.group(1))

    # Add the A1C value if found
    if a1c_match:
        extracted_values["a1c"] = float(a1c_match.group(1))

    # Add the systolic blood pressure value if found
    if systolic_bp_match:
        extracted_values["systolic_bp"] = int(systolic_bp_match.group(1))

    # Add the diastolic blood pressure value if found
    if diastolic_bp_match:
        extracted_values["diastolic_bp"] = int(diastolic_bp_match.group(1))

    # Return the extracted values
    return extracted_values


def extract_diabetic_report_data(text):
    # Initialize empty dictionary to store extracted data
    report_data = {}
    
    # Check if the text mentions HbA1c levels
    if 'HbA1c' in text:
        # Find the line containing HbA1c levels
        hba1c_line = [line for line in text.split('\n') if 'HbA1c' in line][0]
        # Extract the HbA1c value from the line
        hba1c_value = hba1c_line.split(':')[-1].strip()
        # Add HbA1c value to report data dictionary
        report_data['HbA1c'] = hba1c_value
    
    # Check if the text mentions fasting blood glucose levels
    if 'fasting blood glucose' in text:
        # Find the line containing fasting blood glucose levels
        glucose_line = [line for line in text.split('\n') if 'fasting blood glucose' in line][0]
        # Extract the glucose value from the line
        glucose_value = glucose_line.split(':')[-1].strip()
        # Add glucose value to report data dictionary
        report_data['Fasting blood glucose'] = glucose_value
    
    # Check if the text mentions postprandial blood glucose levels
    if 'postprandial blood glucose' in text:
        # Find the line containing postprandial blood glucose levels
        postprandial_line = [line for line in text.split('\n') if 'postprandial blood glucose' in line][0]
        # Extract the postprandial value from the line
        postprandial_value = postprandial_line.split(':')[-1].strip()
        # Add postprandial value to report data dictionary
        report_data['Postprandial blood glucose'] = postprandial_value
        
    # Check if the text mentions glycosylated hemoglobin levels
    if 'glycosylated hemoglobin' in text:
        # Find the line containing glycosylated hemoglobin levels
        hemoglobin_line = [line for line in text.split('\n') if 'glycosylated hemoglobin' in line][0]
        # Extract the hemoglobin value from the line
        hemoglobin_value = hemoglobin_line.split(':')[-1].strip()
        # Add hemoglobin value to report data dictionary
        report_data['Glycosylated hemoglobin'] = hemoglobin_value
        
    # Return the extracted report data dictionary
    return report_data

import re

def extract_values_from_ocr(ocr_text):
    # initialize output dictionary
    values = {}
    
    # search for specific patterns in the OCR text using regular expressions
    # and extract relevant values
    # example patterns for blood report values
    hemoglobin_pattern = r"Hemoglobin\s*([\d\.]+)\s*(\w+)"
    platelet_count_pattern = r"Platelet Count\s*([\d\.]+)\s*(\w+)"
    white_blood_cell_count_pattern = r"White Blood Cell Count\s*([\d\.]+)\s*(\w+)"
    
    # extract values for hemoglobin, platelet count, and white blood cell count
    match = re.search(hemoglobin_pattern, ocr_text, re.IGNORECASE)
    if match:
        value = float(match.group(1))
        unit = match.group(2)
        values["hemoglobin"] = {"value": value, "unit": unit}
    
    match = re.search(platelet_count_pattern, ocr_text, re.IGNORECASE)
    if match:
        value = float(match.group(1))
        unit = match.group(2)
        values["platelet_count"] = {"value": value, "unit": unit}
    
    match = re.search(white_blood_cell_count_pattern, ocr_text, re.IGNORECASE)
    if match:
        value = float(match.group(1))
        unit = match.group(2)
        values["white_blood_cell_count"] = {"value": value, "unit": unit}
    
    # add other patterns to extract more values as needed
    
    return values
