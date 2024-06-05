from flask import Blueprint, request, jsonify, session
from typing import List, Dict
from model.audit_model import Audit
from service.audit_service import AuditService
from service.user_service import UserService

from .schema import NewAuditSchema
from ..util import validate_json

# Create a Blueprint for the audit endpoints
audit = Blueprint('audit', __name__)
audit_service = AuditService()
user_service = UserService()

@audit.route('/', methods=['GET'], strict_slashes=False)
def get_audits():
    """Retrieve all audits with optional sorting.

    This endpoint retrieves all audit records that the user needs to audit.
    It supports optional sorting based on query parameters.

    Returns:
        Response: A JSON response containing a list of documents to be audited.

    Example:
        GET /audits?sort=created_date
        {
            "documents": [
                {
                    "auditUid": "abc456",
                    "documentUid": "abc123",
                    "name": "Document Title",
                    "status": 1,
                    "auditCreatedTime": "2000-09-27T00:00:00Z"
                },
                // Additional documents...
            ]
        }

        Using curl to call endpoint:
            ```bash
            $ curl -i "http://localhost:5000/api/audits?sort=created_date"
            {
                "documents": [
                    {
                        "auditUid": "abc456",
                        "documentUid": "abc123",
                        "name": "Document Title",
                        "status": 1,
                        "auditCreatedTime": "2000-09-27T00:00:00Z"
                        "auditedTime": "2000-09-27T00:00:00Z",
                        "auditor": "Albert",
                    },
                    // Additional documents...
                ]
            }
            ```
    """
    google_id = session['google_id']
    user_id = user_service.get_user_by_google_id(google_id).id
    sort = request.args.get(key = 'sort', default = 'created_date')
    audits = audit_service.get_all_audits(user_id, sort)
    return jsonify({"documents": audits})

@audit.route('/', methods=['POST'], strict_slashes=False)
# FIXME: valid query parameter
# @validate_json(NewAuditSchema)
def request_audit():
    """Request an audit for a document.

    This endpoint creates a new audit record for a specified document
    and assigns it to an auditor identified by their username.

    Request JSON format:
        {
            "documentUid": "abc123",
            "auditorUsername": "albert123"
        }

    Returns:
        Response: A JSON response containing the new audit's UID if creation is successful, otherwise an error message.

    Example:
        POST /audits
        Request Body:
        {
            "documentUid": "abc123",
            "auditorUsername": "albert123"
        }

        Response Body:
        {
            "auditUid": "abc123"
        }

        Using curl to call endpoint:
            * Not exist case
                ```bash
                $ curl -i -X POST "http://localhost:5000/api/audits" \
                    -H "Content-Type: application/json" \
                    -d '{"documentUid": "NotExistUser", "auditorUsername": "NotExistUser"}'

                {
                    "error": "User not found or audit creation failed"
                }
                ```
            * If user exist:
                ```bash
                $ curl -i -X POST "http://localhost:5000/api/audits" \
                    -H "Content-Type: application/json" \
                    -d '{"documentUid": "abc123", "auditorUsername": "albert123"}'
                {
                    "auditUid": "abc123"
                }
                ```
            * Unexpected parameter:
                ```bash
                $ curl -i -X POST "http://localhost:5000/api/audits" \
                    -H "Content-Type: application/json" \
                    -d '{"documentUid": "abc123", "auditorUsername": 123}'
                {
                    "error": "{'auditorUsername': ['Not a valid string.']}"
                }
                ```
    """
    data = request.get_json()
    document_uid = data.get('documentUid')
    auditor_username = data.get('auditorUsername')
    audit = audit_service.create_audit(document_uid, auditor_username)
    if audit:
        return jsonify(audit), 200
    else:
        return jsonify({"error": "User not found or audit creation failed"}), 400
