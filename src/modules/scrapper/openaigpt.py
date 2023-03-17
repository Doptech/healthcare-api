import openai 
from decouple import config

OPEN_AI_API_KEY = config('OPEN_AI_API_KEY', cast=bool)
openai.api_key = OPEN_AI_API_KEY


class OpenAIPrompts():
    
    def __init__(self,prompt):
        self.prompt = None
        self.response = None

    def generate_response(prompt):
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

    def get_text():
        input_text = ("You: ","Hello, how are you?")
        return input_text