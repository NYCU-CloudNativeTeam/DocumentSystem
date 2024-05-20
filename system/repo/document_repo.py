from typing import List
from model.document_model import Document, DocumentComment
from model.base_model import db

class DocumentRepository:
    def get_all_documents(self, sort: str = 'date') -> List[Document]:
        return Document.query.order_by(sort).all()

    def create_document(self, document: Document) -> Document:
        db.session.add(document)
        db.session.commit()
        return document

    def get_document_by_uid(self, uid: str) -> Document:
        return Document.query.filter_by(uid=uid).first()

    def update_document(self, document: Document):
        db.session.commit()
