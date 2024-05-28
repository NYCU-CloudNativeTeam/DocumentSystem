from flask import Blueprint, jsonify, request, current_app
from service.LlmService import LlmService

# define llm as blueprint name
llm = Blueprint('llm', __name__)
llm_service = LlmService()

@llm.route('/', methods=['POST'], strict_slashes=False)
def get_llm_response():
    """
    Send selected text to the backend for processing with a language model and retrieve the result.

    Example:
        Use the following curl command to call the endpoint:
            ```bash
            curl -i -X POST http://localhost:5000/llm \
            -H "Content-Type: application/json" \
            -d '{"question": "Sample text for processing"}'
            ```

    Args:
        None directly, expects a JSON payload with a 'question' field.

        JSON payload format:
            {
                "question": "Sample text for processing"
            }

    Returns:
        JSON response with the processed result from the language model. If the question is empty, it returns an error message.
        
        Expected successful response format:
            {
                "result": "Processed output from LLM"
            }
        
        Error response format:
            {
                "message": "Question cannot be empty"
            }
    """
    json_data = request.get_json()
    question = json_data['question']
    if len(question) < 1:
        return jsonify({"message": "Question cannot be empty"}), 404

    res = llm_service.get_llm_response(question)
    return jsonify({"result": res}), 200