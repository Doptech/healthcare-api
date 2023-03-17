import pytesseract
from PIL import Image
from PIL import Image
from typing import List

from ocr.report import (extract_diabetic_report_high_blood_pressure,
                        extract_diabetic_report_data,
                        extract_values_from_ocr)

class OCR:
    def __init__(self, file_path: str):
        self.file_path = file_path

    def extract_text_from_image(image_path):
        image = Image.open(image_path)
        image = image.convert('L')
        text = pytesseract.image_to_string(image)
        return text

    def extract_re_events(self, text: str) -> List[str]:
        extracted_values_from_ocr = extract_values_from_ocr(text)
        extracted_values_from_ocr_diabetic = extract_diabetic_report_data(text)
        extracted_values_from_ocr_high_blood_pressure = extract_diabetic_report_high_blood_pressure(text)
        return (extracted_values_from_ocr, extracted_values_from_ocr_diabetic, extracted_values_from_ocr_high_blood_pressure)