from flask import current_app
from typing import List, Optional, Dict
from uuid import uuid4

from model.audit_model import Audit
from repo.audit_repo import AuditRepository
from repo.user_repo import UserRepository

class AuditService:
    def __init__(self):
        self.audit_repo = AuditRepository()
        self.user_repo = UserRepository()

    def get_all_audits(self, sort: str) -> List[Dict]:
        """Retrieve all audits with optional sorting.

        Args:
            sort (str): The field by which to sort the audits.

        Returns:
            List[Dict]: A list of dictionaries containing audit details.
        """
        audits = self.audit_repo.get_all_audits(sort)
        audits_list = [
            {
                "auditUid": audit.uid,
                "documentUid": audit.document_id,
                "name": "Document Title",
                "status": audit.audit_status_id,
                "auditCreatedTime": audit.created_date.isoformat() + 'Z'
            }
            for audit in audits
        ]
        current_app.logger.info(f"Get {len(audits_list)} audits record")
        return audits_list

    def create_audit(self, document_uid: str, auditor_username: str) -> Optional[Dict]:
        """Create a new audit record for a document.

        This method first checks if the provided auditor username exists.
        If the user exists, it creates a new audit record with an initial status.

        Args:
            document_uid (str): The unique identifier of the document to be audited.
            auditor_username (str): The username of the auditor who will perform the audit.

        Returns:
            Optional[Dict]: A dictionary containing the new audit's UID if creation is successful, otherwise None.
        """
        user = self.user_repo.find_user_by_username(auditor_username)
        if user:
            audit = Audit(
                uid=str(uuid4()),
                document_id=document_uid,
                creator_id=user.id,
                audit_status_id=1
            )
            new_audit = self.audit_repo.create_audit(audit)
            return {"auditUid": new_audit.uid}
        return None