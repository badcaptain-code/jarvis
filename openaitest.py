import os
import openai
from config import apikey

openai.api_key = "sk-proj-x1MZ6WLqdE6ZOPWAa8pDT3BlbkFJfEUrtoHhBjSkNEauw70f"

response = openai.Completion.create(
    model="text-davinci-003",
    prompt=chatStr,
    temperature=0.7,
    max_tokens=256,
    top_p=1,
    frequency_penalty=0,
    presence_penalty=0
)
    ring(response)
