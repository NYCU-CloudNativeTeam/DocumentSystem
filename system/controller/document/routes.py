from flask import Blueprint, request, jsonify
from model.document_model import Document, DocumentStatus, DocumentComment, DocumentPermission, DocumentPermissionType
from service.DocumentService import DocumentService

# Create a Blueprint for the audit endpoints
document = Blueprint('document', __name__)
document_service = DocumentService()


@document.route('/')
def index():
    return jsonify({"message": "example of document route"}), 200

@document.route('/documents/<string:document_uid>/permissions', methods=['GET'])
def get_document_permissions(document_uid):
    try:
        permissions = document_service.get_document_permissions(document_uid)
        return jsonify({"permissions": permissions}), 200
    except Exception as e:
        current_app.logger.error(f"Error fetching document permissions: {str(e)}")
        return jsonify({"error": "Internal server error"}), 500

@document.route('/documents/<string:document_uid>/permissions', methods=['PUT'])
def update_document_permission(document_uid):
    data = request.get_json()
    if 'username' not in data or 'permissionType' not in data:
        return jsonify({"error": "Username and permissionType fields are required"}), 400

    username = data['username']
    permission_type = data['permissionType']

    try:
        document_service.update_document_permission(document_uid, username, permission_type)
        return jsonify({"message": "Document permission updated successfully"}), 200
    except Exception as e:
        current_app.logger.error(f"Error updating document permission: {str(e)}")
        return jsonify({"error": "Internal server error"}), 500

@document.route('/documents/<string:document_uid>/name', methods=['PUT'])
def update_document_name(document_uid):
    data = request.get_json()
    if 'name' not in data:
        return jsonify({"error": "Name field is required"}), 400
    new_document_name = data['name']
    
    try:
        updated_document = document_service.update_document_name(document_uid, new_document_name)
        if updated_document:
            return jsonify({"message": "Document name updated successfully"}), 200
        else:
            return jsonify({"error": "Document not found"}), 404
    except Exception as e:
        current_app.logger.error(f"Error updating document name: {str(e)}")
        return jsonify({"error": "Internal server error"}), 500