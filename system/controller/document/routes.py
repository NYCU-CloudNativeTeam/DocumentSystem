from flask import Blueprint, request, jsonify

from service.audit_service import AuditService

document = Blueprint('document', __name__)
audit_service = AuditService()

@document.route('/')
def index():
    return jsonify({"message": "example of document route"}), 200

@document.route('/<string:document_uid>/audit-result', methods=['GET'])
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

@document.route('/<string:document_uid>/audit-result', methods=['POST'])
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