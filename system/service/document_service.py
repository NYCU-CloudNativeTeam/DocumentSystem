from typing import List, Dict, Optional
from uuid import uuid4
from flask import current_app
from model.document_model import Document, DocumentComment
from repo.document_repo import DocumentRepository
from repo.user_repo import UserRepository

class DocumentService:
    def __init__(self):
        self.document_repo = DocumentRepository()
        self.user_repo = UserRepository()

    def get_all_documents(self, sort: str) -> Optional[List[Dict]]:
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
        try:
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
        except Exception as e:
            current_app.logger.info(f"Unsupport sorting key: {sort}")
            return None

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

            if is_updated_succesfully == False:
                current_app.logger.error(f"Error when udpate comment for document id: {document.id}")
            else:
                current_app.logger.info(f"Update {len(comments)} comments for document id: {document.id} successfully")

            return is_updated_succesfully
        return None

    def get_document(self, uid: str) -> Optional[Dict]:
        document = self.document_repo.get_document_by_uid(uid)
        if document:
            document_comments = self.document_repo.get_document_comment_by_document_id(document.id)
            current_app.logger.info(f"Get {len(document_comments)} comments of document (uid: {uid})")
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
                        "commentor": {
                            "name": comment.commentor.name,
                        }
                    }
                    for comment in document_comments
                ]
            }
        return None
