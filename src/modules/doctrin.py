from scrapper.openaigpt import OpenAIPrompts
from helperFun import PreProcessor,PostProcessor,zero_shot
from ocr.ocr_layout_parser import OCR 
import re

def start(query,promt_no):
    preprocessor = PreProcessor(query)

    data = preprocessor.preprocess()
    disease = preprocessor.pred_disease() # ner
    if promt_no == 1:
        next_promt,sent_to_openai = zero_shot(data)
        return next_promt, sent_to_openai
    return data,disease

# start("hello my name is om and i wanted to ask about healthcare",promt_no=2)

def docs_ocr(file_paths = None):

    file_data = []
    if file_paths:
        for file in file_paths:
            file_name = file.split('/')[-1]
            ocr_object = OCR(file)
            text = ocr_object.extract_re_events(file)
            file_data.append({file_name:text})

    return file_data    

# print(docs_ocr(file_paths=[r'C:\Users\vrush\OneDrive\Documents\Desktop\healthcare\healthcare-api\src\media\document_sample.pdf']))

def middle(query):
    OpenAIPromptsObject = OpenAIPrompts()
    text = OpenAIPromptsObject.generate_response(query)
    return text

#print(middle("Act like a doctor, what are best meds for high fever for a 10 year child. Medicenes should be in double qoutes"))

def end(response,lat,long,type_of_doc):
    PostProcessorObject = PostProcessor(response)

    meds = re.findall(r'"(.*?)"', response)
    get_nearest_hospital = PostProcessorObject.get_nearby_doc(lat,long,place_type = type_of_doc)

    if len(meds) > 1:
        medical_data = PostProcessorObject.medical_data()
        return medical_data, get_nearest_hospital
    return medical_data

end('"ibuprofen" and "acetaminophen". Be sure to follow the dosage instructions on the packaging and consult a doctor if the fever does not subside after taking the medications.',
10.15,58.5,'any')

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