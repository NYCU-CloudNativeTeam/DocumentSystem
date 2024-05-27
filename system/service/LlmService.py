from flask import current_app

import openai

class LlmService:
    def __init__(self):
        # read GitHub Secrets 中的 API key
        openai.api_key = openai_api_key = os.getenv('OPENAI_API_KEY')

    def get_llm_response(question):
        try:
            response = openai.Completion.create(
                model="gpt-3.5-turbo-0125",
                prompt=f"{question}\n",
                temperature=0.9,
                max_tokens=2048,
                top_p=1,
                frequency_penalty=0,
                presence_penalty=0.6
            )
        except Exception as e:
            print(f"Error: {e}")
            return str(e)
        return response.choices[0].text.strip()