from flask import current_app
import os
import openai

class LlmService:
    def __init__(self):
        openai.api_key = os.getenv('OPENAI_API_KEY')

    def get_llm_response(self, question):
        try:
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are a helpful assistant."},
                    {"role": "user", "content": question}
                ],
                temperature=0.9,
                max_tokens=2048,
                top_p=1,
                frequency_penalty=0,
                presence_penalty=0.6
            )
        except Exception as e:
            print(f"Error: {e}")
            return str(e)
        return response.choices[0].message['content'].strip()