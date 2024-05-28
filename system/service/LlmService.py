from flask import current_app
import os
import openai
from flask import current_app

class LlmService:
    def __init__(self):
        openai.api_key = os.getenv('OPENAI_API_KEY')

    def get_llm_response(self, question):
        try:
            current_app.logger.info(f"accept question: {question}")
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are a document optimization assistant. Your role is to help users correct, optimize, and fill in missing information in their documents. Ensure the content is clear, well-structured, and free of errors. Provide detailed suggestions and improvements where necessary."},
                    {"role": "user", "content": f"Help me correct/optimize the following content and just answer the revised sentence directly.\n\n  {question}"}
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