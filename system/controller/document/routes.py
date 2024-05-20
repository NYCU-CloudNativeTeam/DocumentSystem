from flask import Blueprint, request, jsonify
from typing import List, Dict
from service.document_service import DocumentService
from .schema import NewDocumentSchema, UpdateDocumentSchema
from ..util import validate_json

documents = Blueprint('documents', __name__)
document_service = DocumentService()

@documents.route('/', methods=['GET'], strict_slashes=False)
def get_documents():
    """Retrieve all documents with optional sorting."""
    sort = request.args.get('sort', 'date')
    docs = document_service.get_all_documents(sort)
    return jsonify({"documents": docs})

@documents.route('/', methods=['POST'], strict_slashes=False)
@validate_json(NewDocumentSchema)
def create_document():
    """Create a new document and return its UID."""
    data = request.get_json()
    document_uid = document_service.create_document(data['name'], data['owner_id'], data['document_status_id'])
    return jsonify({"documentUid": document_uid}), 201

@documents.route('/<uid>', methods=['PUT'], strict_slashes=False)
@validate_json(UpdateDocumentSchema)
def update_document(uid):
    """Update the document's body and comments."""
    data = request.get_json()
    document_service.update_document(uid, data['body'], data['comments'])
    return '', 200

@documents.route('/<uid>', methods=['GET'], strict_slashes=False)
def get_document(uid):
    """Retrieve the document details by UID."""
    document = document_service.get_document(uid)
    return jsonify(document)
