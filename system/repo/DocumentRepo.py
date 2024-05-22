from typing import List

from model.document_model import Document, DocumentStatus, DocumentComment, DocumentPermission, DocumentPermissionType
from model.base_model import db

class DocumentRepository:
    """
    Repository class for accessing Document data.
    """

    def get_document_by_uid(self, uid: str) -> Optional[Document]:
        return Document.query.filter_by(uid=uid).first()

    def get_permissions_by_document_uid(self, uid: str) -> List[DocumentPermission]:
        document = self.get_document_by_uid(uid)
        if document:
            return DocumentPermission.query.filter_by(document_id=document.id).all()
        return []

    def get_permission_by_document_and_user(self, document_id: int, user_id: int) -> Optional[DocumentPermission]:
        return DocumentPermission.query.filter_by(document_id=document_id, user_id=user_id).first()

    def save(self, entity) -> None:
        db.session.add(entity)
        db.session.commit()
