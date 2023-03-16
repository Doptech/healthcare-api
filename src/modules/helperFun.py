import re

class PreProcessor():
    
    def __init__(self, data):
        self.data = data
        
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
    
    
