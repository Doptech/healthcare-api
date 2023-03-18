import openai 
from decouple import config

OPEN_AI_API_KEY = config('OPEN_AI_API_KEY')
openai.api_key = OPEN_AI_API_KEY


class OpenAIPrompts():
    
    def __init__(self):
        # self.prompt = prompt
        self.response = None

    def generate_response(sel,prompt):
        completions = openai.Completion.create(
            engine = "text-davinci-003",
            prompt = prompt,
            max_tokens = 1024,
            n = 1,
            stop = None,
            temperature=0.5,
        )
        message = completions.choices[0].text
        return message 