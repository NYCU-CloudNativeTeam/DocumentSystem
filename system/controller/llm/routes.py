from flask import Blueprint, jsonify
from service.llm_service import LlmService

# define llm as blueprint name
llm = Blueprint('llm', __name__)
llm_service = LlmService()

@llm.route('/')
def get_llm_response():
    """
    POST: /llm
    Purpose: Send selected text to the backend for processing with a language model and retrieve the result.
    Example:
        Request:
            {
                "text": "Sample text for processing"
            }
        Response:
            {
                "result": "Processed output from LLM"
            }
    """
    if len(request.form['question']) < 1:
        return jsonify({"message": "Question cannot be empty"}), 404
    question = request.form['question']
    res = llm_service.get_llm_response(question)
    return jsonify({"result": res}), 200
