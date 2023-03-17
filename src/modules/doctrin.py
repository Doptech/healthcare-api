from scrapper.openaigpt import OpenAIPrompts
from .helperFun import PreProcessor,PostProcessor
from ocr.ocr_layout_parser import OCR 
# Pre Porcessing

def zero(text):
    li = []
    sequence = text
    candidate_labels = ['disease', 'hospital', 'health', 'other']
    classifier = pipeline("zero-shot-classification",
                model="facebook/bart-large-mnli") 
    di = classifier(sequence_to_classify, candidate_labels) 
    if (di['labels'][0]) == 'other' :
        prompt = "As a health care bot, I am programmed to discuss topics related to medical care, disease prevention, and overall wellness."
    else:
        prompt = "Act like a health care bot"

    return {'prompt' : prompt}


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
            ocr_object = OCR(file)
            text = ocr_object.extract_re_events()
            file_data.append({file_name:text})
    
    return data,disease,file_data

prepocrssor_main("hi how are you",sound=False, file_paths = r"C:/Users/vrush/OneDrive/Documents/Desktop/healthcare/healthcare-api/src/media/document_sample.jpg")


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

