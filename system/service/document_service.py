from typing import List, Dict, Optional
from uuid import uuid4
from flask import current_app, session
from model.document_model import Document, DocumentPermissionType
from repo.document_repo import DocumentRepository
from repo.user_repo import UserRepository
from repo.audit_repo import AuditRepository
from service.notification_service import NotificationService
from datetime import datetime, timedelta

class DocumentService:
    def __init__(self):
        self.document_repo = DocumentRepository()
        self.user_repo = UserRepository()
        self.audit_repo = AuditRepository()
        self.notification_service = NotificationService()

    def get_all_documents(self, user_id: int, sort: str) -> Optional[List[Dict]]:
        """
        Retrieve a list of all documents sorted by a specified attribute.

        This method queries the document repository to obtain all documents sorted
        according to the provided sorting key. Each document's details are then
        formatted into a dictionary, which includes the document's unique identifier,
        name, and status.

        Args:
            sort (str): The attribute name by which the documents should be sorted.
                        This should be a valid attribute of the Document model.

        Returns:
            Optional[List[Dict]]: A list of dictionaries, where each dictionary
                                contains details of a document. If an exception
                                occurs (e.g., an unsupported sorting key), None
                                is returned.

        Raises:
            None explicitly, but logs an informational message if an exception
            occurs, indicating the unsupported sorting key used.
        """
        def get_document_status(doc, user):
            if doc.owner_id == user.id:
                return 2
            else:
                return self.document_repo.get_permission_by_document_and_user(doc.id, user.id).document_permission_type_id

        def get_document_audit_status(doc):
            audit = self.audit_repo.get_audit_by_document_id(doc.id)
            return audit.audit_status_id if audit else 4

        try:
            user = self.user_repo.find_user_by_id(user_id)
            docs = self.document_repo.get_all_documents(user, sort)
            docs_list = [
                {
                    "uid": doc.uid,
                    "name": doc.name,
                    "status": get_document_status(doc, user),
                    "auditStatus": get_document_audit_status(doc),
                    "body": doc.body,
                }
                for doc in docs
            ]
            return docs_list
        except Exception as e:
            current_app.logger.info(f"Unsupport sorting key: {sort}")
            return None

    def create_document(self, name: str, owner_id: int, document_status_id: int) -> str:
        document = Document(
            uid=str(uuid4()),
            name=name,
            owner_id=owner_id,
            document_status_id=document_status_id,
            lock_session=""
        )
        new_doc = self.document_repo.create_document(document)
        return new_doc.uid

    def update_document(self, uid: str, body: str, comments: List[Dict]):
        document = self.document_repo.get_document_by_uid(uid)
        if document:
            # update document
            document.body = body
            self.document_repo.update_document(document=document)

            # prepare data to udpate document comment
            # transform username into userid
            comments = [{
                    "inline_id": comment.get('inlineId'),
                    "text": comment['text'],
                    "commentor_id": self.user_repo.find_user_by_name(comment['commentor']['name']).id,
                    "document_id": document.id
                } for comment in comments
            ]

            # update document comment
            is_updated_succesfully = self.document_repo.update_document_comments(
                document_id = document.id,
                comments_updates = comments
            )

            audit = self.audit_repo.get_audit_by_document_id(document.id)
            if audit:
                audit.audit_status_id = 4
                self.audit_repo.update_audit(audit)

            if is_updated_succesfully == False:
                current_app.logger.error(f"Error when udpate comment for document id: {document.id}")
            else:
                current_app.logger.info(f"Update {len(comments)} comments for document id: {document.id} successfully")

            return is_updated_succesfully
        return None

    def get_document(self, user_id: str, document_uid: str) -> Optional[Dict]:
        document = self.document_repo.get_document_by_uid(document_uid)
        if document:
            user = self.user_repo.find_user_by_id(user_id)
            document = self.document_repo.get_document_by_uid(document_uid)
            mode = self.document_repo.get_document_mode(user, document)
            audit_status = self.audit_repo.get_audit_by_document_id(document.id)
            audit_status_id = audit_status.audit_status_id if audit_status else 4
            document_comments = self.document_repo.get_document_comment_by_document_id(document.id)
            otherIsEditting = False
            current_app.logger.info(f"Get {len(document_comments)} comments of document (uid: {document_uid})")
            if document.lock_session is not "" and document.lock_session is not None:
                if document.lock_session != session.get("lock_session"):
                    lock_session = datetime.strptime(document.lock_session, "%Y-%m-%d %H:%M:%S")
                    if lock_session + timedelta(minutes=5) > datetime.now() :
                        current_app.logger.info(f"Document Ud: {document_uid} is locked by other user.")
                        otherIsEditting = True
            document.lock_session = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            session["lock_session"] = document.lock_session
            self.document_repo.update_document(document)
            return {
                'otherIsEditting': otherIsEditting,
                "uid": document.uid,
                "name": document.name,
                "body": document.body,
                "otherIsEditing": bool(document.lock_session),
                "mode": mode,
                "auditStatus": audit_status_id,
                "comments": [
                    {
                        "inlineId": comment.inline_id,
                        "text": comment.text,
                        "commentor": {
                            "name": self.user_repo.find_user_by_id(comment.commenter_id).name,
                        }
                    }
                    for comment in document_comments
                ]
            }
        current_app.logger.info(f"Can't find document by uid: {document_uid}")
        return {"state": "Cant find document by uid"}

    def delete_lock_session_by_uid(self, uid: str):
        document = self.document_repo.get_document_by_uid(uid)
        if document:
            if session.get("lock_session") == document.lock_session:
                document.lock_session = None
                self.document_repo.update_document(document)
                session.pop('lock_session', None)
                return {"state": "true"}
        return {"state": "false"}

    def update_lock_session_by_uid(self, uid: str):
        document = self.document_repo.get_document_by_uid(uid)
        if document:
            if session.get("lock_session") == document.lock_session:
                document.lock_session = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                session["lock_session"] = document.lock_session
                self.document_repo.update_document(document)
                return {"state": "true", "lock_session": document.lock_session}
        return {"state": "false"}

    def delete_document_by_uid(self, document_uid: str):
        """Delete a document from the database identified by its unique identifier (UID).

        This method attempts to find a document by its UID. If the document is found,
        it is deleted from the database. If the document is not found, it logs this information
        and returns False. If any exception occurs during the process,
        it logs the error and also returns False.

        Args:
            document_uid (str): The unique identifier of the document to be deleted.

        Returns:
            bool: True if the document is successfully deleted, False otherwise.
                False is returned both in the case where the document is not found
                and in the case where an exception occurs.
        """
        try:
            document = self.document_repo.get_document_by_uid(document_uid)
            if document:
                current_app.logger.info(f"Delete document UID: {document_uid}")
                self.document_repo.delete_document(document)
                return True
            else:
                current_app.logger.info(f"No document found with UID: {document_uid}")
                return False
        except Exception as e:
            current_app.logger.error(f"Error when attempting to delete document with UID: {document_uid}")
            current_app.logger.error(e)
            return False

    def document_reminder(self, document_uid: str):
        try:
            # get document first
            document = self.document_repo.get_document_by_uid(document_uid)
            if document:
                # get auditor by document id
                audit = self.audit_repo.get_audit_by_document_id(document.id)

                # search username
                auditor = self.user_repo.find_user_by_id(audit.creator_id)
                current_app.logger.info(
                    f"Found user id: {auditor.id}, name: {auditor.name}, "
                    f"username: {auditor.username} of document UID: {document_uid}"
                )

                # send notifitication
                self.notification_service.publisher_to_queue(
                    third_party = "email",
                    title = "New Document Review Notification",
                    content = f"Dear {auditor.name},"
                        f"You have new document review"
                        f"Please login to system to review",
                    recipient = f"{auditor.mail}",
                )
                return True
            else:
                current_app.logger.info(f"No document found with UID: {document_uid}")
                return False
        except Exception as e:
            current_app.logger.error(f"Error when attempting to notify to auditor of document UID: {document_uid}")
            current_app.logger.error(e)
            return False

    def get_document_permissions(self, user_id: int, document_uid: str) -> List[Dict]:
        document_id = self.document_repo.get_document_by_uid(document_uid).id
        document_permissions = self.document_repo.get_permissions(user_id, document_id)
        current_app.logger.info(f"Get {len(document_permissions)} document record of document uid: {document_uid}")
        if document_permissions:
            permissions_list = []
            for perm in document_permissions:
                user = self.user_repo.find_user_by_id(perm.user_id)
                if user:
                    permissions_list.append({
                        "name": user.name,
                        "username": user.username,
                        "permissionType": perm.document_permission_type_id
                    })
                else:
                    # cannot find user by user ID in permissions
                    current_app.logger.info(f"Cannot get user by user ID in permissions {perm.user_id}")
                    return None

            return permissions_list
        else:
            # cannot find permissions by UID
            current_app.logger.info(f"Cannot get permissions by document UID {document_uid}")
            return None

    def update_document_permission(self, uid: str, username: str, permission_type: int) -> bool:
        document = self.document_repo.get_document_by_uid(uid)
        if self.document_repo.is_document_permission_type_exist(permission_type) == False:
            current_app.logger.info(f"Document permisssion type: {permission_type} not exist")
            return False

        if document:
            user = self.user_repo.find_user_by_username(username)
            if user:
                document_permission = self.document_repo.get_permission_by_document_and_user(document.id, user.id)
                if document_permission:
                    document_permission.document_permission_type_id = permission_type
                    self.document_repo.update_document_permission(document_permission)
                    current_app.logger.info(f"update from {document_permission.document_permission_type_id} to {permission_type}")
                    return True
                else:
                    # current_app.logger.info(f"Error! Cannot get document_permission by document and user ID: {document.id}, {user.id}")
                    document_permission = self.document_repo.add_document_permission(user, document, permission_type)
                    return True
            else:
                current_app.logger.info(f"Error! Cannot get user by username {username}")
                return None
        else:
            current_app.logger.info(f"Error! Cannot get document by document_uid")
            return None

    def update_document_name(self, uid: str, new_document_name: str) -> Optional[Document]:
        document = self.document_repo.get_document_by_uid(uid)
        if document:
            document.name = new_document_name
            self.document_repo.update_document(document)
            return document
        else:
            current_app.logger.info(f"Error! Cannot get document by document_uid {uid}")
            return None

    def write_document_permission_type(
        self,
        name: str
    ):
        document_permission_type = DocumentPermissionType(name=name)
        new_document_permission_type = self.document_repo.create_document_permission_type_not_exist(document_permission_type)
        return new_document_permission_type
