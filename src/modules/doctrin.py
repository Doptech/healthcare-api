from scrapper.openaigpt import OpenAIPrompts
from .helperFun import PreProcessor,PostProcessor
from ocr.report import OCR 
# Pre Porcessing

def prepocrssor_main(data,sound=False, file_paths = None):
    
    """
    - Cleaning the data
    - NER 
    - Take Onbarding Data
    - Files inputted should be sent to ocr & take inmport data & ocr with them  --> Summarize it
    - Base QUERY MODEL SENDER

    """
    
    
    if sound:
        data = PreProcessor.wav_to_transcript(data)
    # data which for SA
    preprocessor = PreProcessor(data)
    data = preprocessor.preprocess()
    disease = preprocessor.pred_disease(1024) # ner
    
    file_data = []
    if file_paths:
        for file in file_paths:
            file_name = file.split('/')[-1]
            data = OCR(file).extract_re_events()
            file_data.append({file_name:data})
    
    return data,disease,file_data


# Main'
prepocrssor_main("",sound=False, file_paths = None)
OpenAIPromptsObject = OpenAIPrompts()

# Post Processing

PostProcessorObject = PostProcessor()
medical_data = PostProcessorObject.medical_data()
get_nearest_hospital = PostProcessorObject.get_nearby_doc()

"""
- take the desises from ner
- from a bohot abstract template for the answer
- Refrence the data from the google sheets
- send the answer to the user

"""

