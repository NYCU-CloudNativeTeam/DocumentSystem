from flask import current_app
from typing import List, Optional, Dict
from uuid import uuid4

from model.document_model import Document, DocumentStatus, DocumentComment, DocumentPermission, DocumentPermissionType
from repo.DocumentRepo import DocumentRepository

class DocumentService:
    def __init__(self):
        self.document_repo = DocumentRepository()
        self.user_repo = UserRepository()
    
    def get_document_permissions(self, uid: str) -> List[Dict]:
        document_permissions = self.document_repo.get_permissions_by_document_uid(uid)
        permissions_list = []
        for perm in document_permissions:
            user = self.user_repo.find_user_by_id(perm.user_id)
            permissions_list.append({
                "username": user.username,
                "mail": user.mail,
                "permissionType": perm.document_permission_type_id
            })
        return permissions_list
    
    def update_document_permission(self, uid: str, username: str, permission_type: int) -> None:
        document = self.document_repo.get_document_by_uid(uid)
        if not document:
            raise ValueError("Document not found")

        user = self.user_repo.find_user_by_username(username)
        if not user:
            raise ValueError("User not found")

        document_permission = self.document_repo.get_permission_by_document_and_user(document.id, user.id)
        if not document_permission:
            raise ValueError("Document permission not found")

        document_permission.document_permission_type_id = permission_type
        self.document_repo.save(document_permission)
    
    def update_document_name(self, uid: str, new_document_name: str) -> Optional[Document]:
        document = self.document_repo.get_document_by_uid(uid)
        if document:
            document.name = new_document_name
            self.document_repo.save(document)
            return document
        return None