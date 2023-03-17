import re
import whisper
import spacy
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
from googleplaces import GooglePlaces, types, lang
from scrapper.google import google_search
from decouple import config
from transformers import pipeline

GOOLGLE_MAP_API_KEY = config('GOOLGLE_MAP_API_KEY', cast=bool)
  
class PreProcessor():
    
    def __init__(self, data):
        self.data = data
        
    def wav_to_transcript(wav_file_path,model_name="base", segments = False):
        model = whisper.load_model(model_name)
        result = model.transcribe(wav_file_path)
        if segments:
            for segment in result['segments']:
                segment.pop('tokens')
                segment.pop('temperature')
                segment.pop('avg_logprob')
                segment.pop('compression_ratio')
                segment.pop('no_speech_prob')
            return result['segments']
        return result
    
    def query(a1,a2,a3,a4,a5):
        query = f"I am having {a1} pre-existing medical condition. {a2} medications , supplements taken. {a3} surgeries or hospitalizations done. {s4} change appetite, energy levels, or sleep patterns is observed. {a5} are the sympthoms observed "
        return query
    

   

    def preprocess(self):
        # clean data using regex
        text = self.data['text']
        text = re.sub(r'[^a-zA-Z0-9\s]', '', text)
        return self.data
    
    def pred_disease(text): # {'DISEASE': ['diarrhea']} ex output
        nlp = spacy.load('en_disease_pipeline')
        doc = nlp(text)
        values_list = []
        diseases_list = {}
        for ent in nlp(doc).ents:
            values_list.append(ent.text.strip())
            
        diseases_list['DISEASE'] = values_list
        return diseases_list

    
    def summarization(self,TO_SUMMARIZE):
        tokenizer = AutoTokenizer.from_pretrained("mse30/bart-base-finetuned-pubmed")
        model = AutoModelForSeq2SeqLM.from_pretrained("mse30/bart-base-finetuned-pubmed")
        inputs = tokenizer([TO_SUMMARIZE], max_length=1024, return_tensors="pt")

        # Generate Summary
        summary_ids = model.generate(inputs["input_ids"],min_length=0, max_length=20)
        return tokenizer.batch_decode(summary_ids, skip_special_tokens=True, clean_up_tokenization_spaces=False)[0]

class PostProcessor():
    
    def __init__(self, data):
        self.data = data
        
    def medical_data(self,meds:list):
        res = {}
        for med in meds:
            text_retrived = google_search(med)
            res[med] = text_retrived
            
        return res
    
    def get_nearby_doc(self,lat, lng, place_type):
  
        google_places = GooglePlaces(GOOLGLE_MAP_API_KEY)

        # Call the nearby_search function with the given latitude, longitude, and place type
        query_result = google_places.nearby_search(
            lat_lng = {'lat': lat, 'lng': lng},
            radius = 5000,
            types = [place_type]
        )

        locations = {}
        for place in query_result.places:
            location_details = {
                'name': place.name,
                'latitude': place.geo_location['lat'],
                'longitude': place.geo_location['lng']
            }
            locations[place.place_id] = location_details

        return locations
    

   

"""def set_model_variable(user_query):
    retrival_model = False
    gpt_neo_model = False

    # check if user query is a small talkative sentence
    if len(user_query.split()) <= 5:
        gpt_neo_model = True

    # check if user query is of 3-4 sentences
    elif len(user_query.split('.')) >= 3 and len(user_query.split('.')) <= 4:
        retrival_model = True

    # check if user query is not a question
    elif '?' not in user_query:
        gpt_neo_model = True

    return {'retrival_model': retrival_model, 'gpt_neo_model': gpt_neo_model}"""
