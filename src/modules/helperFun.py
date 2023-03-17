import re
import whisper
import spacy
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM

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
    
    def preprocess(self):
        # clean data using regex
        text = self.data['text']
        text = re.sub(r'[^a-zA-Z0-9\s]', '', text)
        return self.data

    def queryLen_based_removal(self, query_len):
        if len(self.data['text']) < query_len:
            # then we can use neo gpt
            return None
        # then we can use retriever
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

def set_model_variable(user_query):
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

    return {'retrival_model': retrival_model, 'gpt_neo_model': gpt_neo_model}
