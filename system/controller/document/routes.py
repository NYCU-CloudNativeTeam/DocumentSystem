from typing import List, Dict

from flask import Blueprint, request, jsonify, current_app
from service.document_service import DocumentService
from service.audit_service import AuditService
from .schema import NewDocumentSchema, UpdateDocumentSchema
from ..util import validate_json

documents = Blueprint('documents', __name__)

document_service = DocumentService()
audit_service = AuditService()

@documents.route('/', methods=['GET'], strict_slashes=False)
def get_documents():
    """
    Retrieve all documents with optional sorting.

    Example:
        Use the following curl command to call the endpoint with sorting by 'name':
            ```bash
            curl -i -X GET 'http://localhost:5000/api/documents/?sort=name'
            ```

    Args:
        sort (str): Query parameter to specify sorting of documents. Default is 'date'.

    Returns:
        JSON response containing a list of documents.
    """
    sort = request.args.get('sort', 'created_date')
    docs = document_service.get_all_documents(sort)
    return jsonify({"documents": docs})

@documents.route('/', methods=['POST'], strict_slashes=False)
@validate_json(NewDocumentSchema)
def create_document(name, owner_id, document_status_id):
    """
    Create a new document based on provided data and return its unique identifier (UID).

    This endpoint requires a JSON payload that includes the document's name, the owner's ID, 
    and the document status ID. The document is then created in the database, and its UID is returned.

    Example:
        Use the following curl command to create a new document:
            ```bash
            curl -i -X POST http://localhost:5000/api/documents/ \
            -H "Content-Type: application/json" \
            -d '{
                "name": "Project Proposal",
                "owner_id": 1,
                "document_status_id": 2
            }'
            ```

    Returns:
        JSON response with the UID of the newly created document.
    """
    document_uid = document_service.create_document(name, owner_id, document_status_id)
    return jsonify({"documentUid": document_uid}), 201

@documents.route('/<uid>', methods=['PUT'], strict_slashes=False)
@validate_json(UpdateDocumentSchema)
def update_document(uid, body, comments):
    """Update the document's body and comments based on provided UID and validated JSON.

    Args:
        uid (str): The unique identifier of the document.
        body (str): The new content of the document's body.
        comments (str): The updated comments associated with the document.

    Returns:
        An empty HTTP 200 response indicating successful update.

    Example:
        Use the following curl command to update a new document:
            ```bash
            curl -i -X PUT http://localhost:5000/api/documents/doc1 \
            -H "Content-Type: application/json" \
            -d '{
                "body": "Updated body of the document.",
                "comments": [
                    {
                        "inlineId": 123,
                        "text": "Important comment here.",
                        "commentor": {
                            "name": "Adam"
                        }
                    }
                ]
            }'
            ```
    """
    document_service.update_document(uid, body, comments)
    return '', 200

@documents.route('/<uid>', methods=['GET'], strict_slashes=False)
def get_document(uid):
    """
    Retrieve the document details by its unique identifier (UID).

    This endpoint fetches detailed information about a specific document using its UID. 
    It returns a JSON object containing all pertinent details of the document if found. 
    If the document cannot be located, it returns a JSON response indicating that no document 
    was found with the provided UID.

    Args:
        uid (str): The unique identifier of the document to retrieve.

    Returns:
        JSON: A JSON response containing detailed information about the document, or an error message if not found.

    Example:
        Use the following curl command to retrieve a document by UID:
            ```bash
            curl -i -X GET http://localhost:5000/api/documents/doc1
            ```
    """
    document = document_service.get_document(uid)
    return jsonify(document)

@documents.route('/<string:document_uid>/audit-result', methods=['GET'])
def get_audit_result(document_uid):
    """
    Retrieve the audit result for a specific document identified by its UID.

    Args:
        document_uid (str): The unique identifier for the document.

    Returns:
        A JSON response containing the audit results if found, or an error message if not found.
    """
    audit_result = audit_service.get_audit_result(document_uid)
    if audit_result:
        return jsonify(audit_result), 200
    else:
        return jsonify({"error": "Audit record not found"}), 400

@documents.route('/<string:document_uid>/audit-result', methods=['POST'])
def submit_audit_result(document_uid):
    """
    Submit or update the audit result for a specific document based on the provided UID.

    This endpoint expects a JSON payload containing the audit UID, 
    audit status, and an optional rejected reason.
    
    Args:
        document_uid (str): The unique identifier for the document.

    Returns:
        A JSON response indicating whether the audit status was successfully updated or if the update failed.
    """
    try:
        data = request.get_json()
        # Possible values: "approved(1)", "rejected(2)", "pending(3)"
        audit_status = data.get('auditStatus')
        rejected_reason = data.get('rejectedReason')

        audit_result = audit_service.submit_audit_result(
            document_uid = document_uid,
            audit_status = audit_status, 
            rejected_reason = rejected_reason
        )

        if audit_result:
            return jsonify({"message": "Audit status updated successfully"}), 200
        else:
            return jsonify({"error": "Failed to update audit status"}), 400
    except KeyError as e:
        return jsonify(error=f"Missing parameter: {str(e)}"), 400
