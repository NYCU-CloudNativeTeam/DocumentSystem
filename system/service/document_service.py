from typing import List, Dict, Optional
from uuid import uuid4
from model.document_model import Document, DocumentComment
from repo.document_repo import DocumentRepository
from repo.user_repo import UserRepository

class DocumentService:
    def __init__(self):
        self.document_repo = DocumentRepository()
        self.user_repo = UserRepository()

    def get_all_documents(self, sort: str) -> List[Dict]:
        docs = self.document_repo.get_all_documents(sort)
        docs_list = [
            {
                "uid": doc.uid,
                "name": doc.name,
                "status": doc.document_status_id,
            }
            for doc in docs
        ]
        return docs_list

    def create_document(self, name: str, owner_id: int, document_status_id: int) -> str:
        document = Document(
            uid=str(uuid4()),
            name=name,
            owner_id=owner_id,
            document_status_id=document_status_id
        )
        new_doc = self.document_repo.create_document(document)
        return new_doc.uid

    def update_document(self, uid: str, body: str, comments: List[Dict]):
        document = self.document_repo.get_document_by_uid(uid)
        if document:
            document.body = body
            document.comments = [
                DocumentComment(
                    inline_id=comment.get('inlineId'),
                    text=comment['text'],
                    commenter_id=self.user_repo.find_user_by_name(comment['commenter']['name']).id,
                    document_id=document.id
                )
                for comment in comments
            ]
            self.document_repo.update_document(document)

    def get_document(self, uid: str) -> Optional[Dict]:
        document = self.document_repo.get_document_by_uid(uid)
        if document:
            return {
                "uid": document.uid,
                "name": document.name,
                "body": document.body,
                "otherIsEditing": bool(document.lock_session),
                "mode": document.document_status_id,
                "comments": [
                    {
                        "inlineId": comment.inline_id,
                        "text": comment.text,
                        "commenter": {
                            "name": comment.commenter.name,
                        }
                    }
                    for comment in document.comments
                ]
            }
        return None
