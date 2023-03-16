import re
import whisper
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
    
    def summarization(self,ARTICLE_TO_SUMMARIZE):
        tokenizer = AutoTokenizer.from_pretrained("ccdv/lsg-bart-base-16384-pubmed")
        model = AutoModelForSeq2SeqLM.from_pretrained("ccdv/lsg-bart-base-16384-pubmed")
        
        inputs = tokenizer([ARTICLE_TO_SUMMARIZE], max_length=1024, return_tensors="pt")

        # Generate Summary
        summary_ids = model.generate(inputs["input_ids"], num_eams=2, min_length=0, max_length=20)
        tokenizer.batch_decode(summary_ids, skip_special_tokens=True, clean_up_tokenization_spaces=False)[0]
        return model.generate(inputs["input_ids"], num_eams=2, min_length=0, max_length=20)
