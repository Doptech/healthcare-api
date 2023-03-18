from scrapper.openaigpt import OpenAIPrompts
from helperFun import PreProcessor,PostProcessor
from ocr.ocr_layout_parser import OCR 
from transformers import pipeline

def start(query,promt_no):
    preprocessor = PreProcessor(query)

    data = preprocessor.preprocess()
    disease = preprocessor.pred_disease() # ner
    if promt_no == 1:
        next_promt,sent_to_openai = zero_shot(data)
        return next_promt, sent_to_openai
    return data,disease

def docs_ocr(file_paths = None):

    file_data = []
    if file_paths:
        for file in file_paths:
            file_name = file.split('/')[-1]
            ocr_object = OCR(file)
            text = ocr_object.extract_re_events(file)
            file_data.append({file_name:text})

    return file_data    


def middle(query):
    OpenAIPromptsObject = OpenAIPrompts(query)
    text = OpenAIPromptsObject.generate_response()
    return text

def end(response,lat,long,type_of_doc):
    PostProcessorObject = PostProcessor()

    meds = response.split("|")
    get_nearest_hospital = PostProcessorObject.get_nearby_doc(lat,long,place_type = type_of_doc)

    if len(meds) > 1:
        medical_data = PostProcessorObject.medical_data()
        return medical_data, get_nearest_hospital
    return medical_data

"""EXTRA FUNCTIONS"""

def zero_shot(text):
    li = []
    sequence = text
    candidate_labels = ['disease', 'hospital', 'health', 'other']
    classifier = pipeline("zero-shot-classification",
                model="facebook/bart-large-mnli") 
    di = classifier(text, candidate_labels) 
    if (di['labels'][0]) == 'other' :
        prompt = "As a health care bot, I am programmed to discuss topics related to medical care, disease prevention, and overall wellness."
    else:
        prompt = "Act like a health care bot"

    return {'prompt' : prompt}

"""
    - Cleaning the data
    - NER 
    - Take Onbarding Data
    - Files inputted should be sent to ocr & take inmport data & ocr with them  --> Summarize it
    - Base QUERY MODEL SENDER
    - take the desises from ner
    - from a bohot abstract template for the answer
    - Refrence the data from the google sheets
    - send the answer to the user
    
"""