from flask import current_app
from typing import List, Optional, Dict
from uuid import uuid4

from model.audit_model import Audit, AuditStatus
from repo.document_repo import DocumentRepository
from repo.audit_repo import AuditRepository
from repo.user_repo import UserRepository

class AuditService:
    def __init__(self):
        self.document_repo = DocumentRepository()
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
            audit_status = AuditStatus(
                name = auditor_username,
                # possible values: "approved(1)", "rejected(2)", "pending(3)"
                # default is pending
                audit_status_value = 3
            )
            new_audit_status = self.audit_repo.create_audit_status(audit_status)
            current_app.logger.info(f"New audits status record {new_audit_status}")
            audit = Audit(
                uid = str(uuid4()),
                document_id = document_uid,
                creator_id = user.id,
                audit_status_id = audit_status.id
            )
            new_audit = self.audit_repo.create_audit(audit)
            current_app.logger.info(f"New audits record {new_audit}")
            return {"auditUid": new_audit.uid}
        return None

    def get_audit_result(self, document_uid: str) -> Optional[Dict]:
        """
        Retrieve the audit result for a given document by its unique identifier (UID).

        This method fetches the audit record associated with the provided document UID. It then retrieves the
        status of the audit and constructs a dictionary containing details of the audit, such as the audit's UID,
        document UID, status, auditor's details, and timing of the audit. Depending on the status of the audit,
        additional fields like 'rejectedReason' might be included.

        Args:
            document_uid (str): The unique identifier for the document whose audit result is to be retrieved.

        Returns:
            Optional[Dict]: A dictionary containing detailed audit results if found. The dictionary includes:
                - auditUid: The UID of the audit.
                - documentUid: The UID of the document.
                - auditStatus: The current status of the audit
                                - 1: approved
                                - 2: rejected
                                - 3: pending).
                - auditor: Information about the auditor.
                - auditedTime: The timestamp when the audit status was last updated.
                - rejectedReason: The reason for rejection.
        """
        document = self.document_repo.get_document_by_uid(document_uid)
        if document:
            document_id = document.id
            audit = self.audit_repo.get_audit_by_document_id(document_id)
            if audit:
                audit_status = self.audit_repo.get_audit_status_by_audit_status_id(audit.audit_status_id)
                if audit_status:
                    print("audit_status", audit_status)
                    audit_status_value = audit_status.audit_status_value
                    print("audit_status_value", audit_status_value)
                    current_app.logger.info(f"audit_result is {audit_status_value}")
                    # possible values 1 means approved
                    if audit_status_value == 1:
                        auditor = self.user_repo.find_user_by_name(audit_status.name)
                        audit_result = {
                            'auditUid': audit.uid,
                            'documentUid': document_uid,
                            'auditStatus': audit_status.audit_status_value,
                            'auditor': {
                                "userId": auditor.id,
                                "username": auditor.username,
                                "name": auditor.name
                            },
                            'auditedTime': audit_status.updated_date.isoformat() + 'Z'
                        }
                    # 2 means rejected
                    elif audit_status_value == 2:
                        auditor = self.user_repo.find_user_by_name(audit_status.name)
                        print("auditor", auditor)
                        audit_result = {
                            'auditUid': audit.uid,
                            'documentUid': document_uid,
                            'auditStatus': audit_status.audit_status_value,
                            'rejectedReason': audit.rejected_reason,
                            'auditor': {
                                "userId": auditor.id,
                                "username": auditor.username,
                                "name": auditor.name
                            },
                            'auditedTime': audit_status.updated_date.isoformat() + 'Z'
                        }
                    # 3 means pending
                    elif audit_status_value == 3:
                        auditor = self.user_repo.find_user_by_name(audit_status.name)
                        audit_result = {
                            'auditUid': audit.uid,
                            'documentUid': document_uid,
                            'auditStatus': audit_status.audit_status_value,
                            'auditor': {
                                "userId": auditor.id,
                                "username": auditor.username,
                                "name": auditor.name
                            },
                        }
                    else:
                        audit_result = None
                        current_app.logger.info(f"Error! audit_result is not match 1, 2, 3.")
                    return audit_result
                else:
                    current_app.logger.info(f"Error! Cannot get audit_status by audit_status_id")
                    return None
            else:
                current_app.logger.info(f"Error! Cannot get audit by document_id")
                return None
        else:
            current_app.logger.info(f"Error! Cannot get document by document_uid")
            return None

    
    def submit_audit_result(
        self,
        document_uid: str,
        audit_status: int,
        rejected_reason: str
    ):
        """
        Update the audit status and rejected reason for a specific document based on the document UID.

        This method checks if the document's current audit status is 'pending'. If so, it updates the
        audit status and rejected reason in the audit records. Logs are generated for each significant
        action, including failure to find the document or its audit status, as well as the outcomes of
        updates.

        Args:
            document_uid (str): The unique identifier for the document whose audit result needs updating.
            audit_status (int): The new audit status to be set if the current status is 'pending'.
                                Possible values are:
                                - 1: 'approved'
                                - 2: 'rejected'
                                - 3: 'pending'
            rejected_reason (str): The reason for rejection, relevant if the new audit status is 'rejected'.

        Returns:
            bool: True if the audit status and rejected reason were successfully updated, False otherwise.
                Returns None if no audit record is found for the given document UID or the specific
                audit status does not exist.
        """
        # search document by UID
        document = self.document_repo.get_document_by_uid(document_uid)
        if document:
            document_id = document.id
            audit = self.audit_repo.get_audit_by_document_id(document_id)

            if audit:
                # if document exist, get document audit status currently
                origion_audit_status = self.audit_repo.get_audit_status_by_audit_status_id(audit.audit_status_id)
                if origion_audit_status:
                    # possible values: "approved(1)", "rejected(2)", "pending(3)"
                    # get current audit status value
                    origion_audit_status_value = origion_audit_status.audit_status_value
                    print("origion_audit_status_value", origion_audit_status_value)
                    
                    # if document still pending, update to new audit status
                    if origion_audit_status_value == 3:
                        # update reject reason for document in audit table
                        audit.rejected_reason = rejected_reason
                        self.audit_repo.update_audit(audit)
                        current_app.logger.info(f"Update reject reason: {rejected_reason} for document UID {document_uid}")

                        # update audit status value for audit status UID
                        origion_audit_status.audit_status_value = audit_status
                        audit_status_id = origion_audit_status.id
                        self.audit_repo.update_audit_status(origion_audit_status)
                        current_app.logger.info(f"Update audit_status_value to {audit_status} for audit status ID {audit_status_id} .")
                        return True
                    else:
                        current_app.logger.info(f"audit_status_value is {origion_audit_status_value}, {document_uid} had been auditted.")
                        return False
                else:
                    current_app.logger.info(f"Cannot get audit_status by audit_status_id {audit.audit_status_id}")
                    return None
            else:
                # cannot find document by UID
                current_app.logger.info(f"Cannot get audit by document_uid {document_uid}")
                return None
        else:
            current_app.logger.info(f"Error! Cannot get document by document_uid")
            return None