from typing import List
from flask import current_app
from model.document_model import (
    Document,
    DocumentStatus,
    DocumentComment,
    DocumentPermission,
    DocumentPermissionType
)
from model.user_model import User
from model.audit_model import Audit
from model.base_model import db
from sqlalchemy import or_

class DocumentRepository:
    def get_all_documents(self, user: User, sort: str = 'date') -> List[Document]:
        return Document.query.\
            join(DocumentPermission, DocumentPermission.document_id == Document.id, isouter=True).\
            filter(or_(DocumentPermission.user_id == user.id, Document.owner_id == user.id)).\
            order_by(sort).\
            all()

    def create_document(self, document: Document) -> Document:
        db.session.add(document)
        db.session.commit()
        return document

    def get_document_by_uid(self, uid: str) -> Document:
        return Document.query.filter_by(uid=uid).first()

    def update_document(self, document: Document):
        db.session.commit()

    def get_permissions(self, user_id: int, document_id: str) -> List[DocumentPermission]:
        return DocumentPermission.query.\
            filter_by(document_id=document_id).\
            filter(DocumentPermission.user_id != user_id).\
            join(Document, Document.id == DocumentPermission.document_id).\
            filter(Document.owner_id != DocumentPermission.user_id).\
            all()

    def get_permission_by_document_and_user(self, document_id: int, user_id: int) -> DocumentPermission:
        return DocumentPermission.query.filter_by(document_id=document_id, user_id=user_id).first()

    def update_document_permission(self, document_permission: DocumentPermission) -> None:
        db.session.commit()

    def add_document_permission(self, user: User, document: Document, document_permission_type_id: int) -> None:
        permission = DocumentPermission(
            user_id=user.id,
            document_id=document.id,
            document_permission_type_id=document_permission_type_id
        )
        db.session.add(permission)
        db.session.commit()

    def create_document_status(self, document_status: DocumentStatus) -> DocumentStatus:
        """Add a new user to the database.

        Args:
            user (User): The user instance to be added.

        Returns:
            User: The newly added user instance.
        """
        db.session.add(document_status)
        db.session.commit()
        return document_status

    def update_document_comments(
        self,
        document_id,
        comments_updates: List[dict]
    ) -> bool:
        """
        Partially update comments for a specific document based on the provided updates.

        This function fetches comments associated with a given document by their
        unique identifier (document_id), and applies updates specified in the comments_updates list.
        If cannot find inline_id means new comment, also write to database.
        Each entry in the list should include the unique inline identifier for the comment and
        the fields to be updated.

        Args:
            document_id (int): The unique identifier of the document whose comments are to be updated.
            comments_updates (list): A list of dictionaries containing updates for each comment.
                                    Each dictionary must include the 'inlineId' of the comment
                                    and the fields to be updated, such as 'text'.

        Returns:
            bool: Returns True if all specified comments are successfully updated, False otherwise.
        """
        try:
            for update in comments_updates:
                comment = DocumentComment.query.filter_by(
                    document_id=document_id,
                    inline_id=update['inline_id']
                ).first()

                if comment:
                    # Update existing comment
                    comment.text = update['text']
                    comment.comment_id = update['commentor_id']
                else:
                    # Create new comment
                    new_comment = DocumentComment(
                        document_id=document_id,
                        inline_id=update['inline_id'],
                        text=update['text'],
                        commenter_id=update['commentor_id']
                    )
                    db.session.add(new_comment)

            db.session.commit()
            return True
        except Exception as e:
            current_app.logger.error(f"Error when updated comment for document_id: {document_id}")
            current_app.logger.error(e)
            return False


    def get_document_comment_by_document_id(self, document_id: str) -> list[DocumentComment]:
        """
        Retrieve all comments associated with a specific document.

        This method queries the database for all comments linked to a given document ID.
        It returns a list of DocumentComment model instances. If no comments are found, an empty list is returned.

        Args:
            document_id (int): The unique identifier of the document for which comments are being retrieved.

        Returns:
            List[DocumentComment]: A list of DocumentComment model instances that are associated with the document.
        """
        return DocumentComment.query.filter_by(document_id=document_id).all()

    def delete_document(self, document: Document) -> bool:
        """Delete a document given found document of database

        Args:
            document (Document): The document instance to be deleted.

        Returns:
            None
        """
        Audit.query.filter_by(document_id=document.id).delete()
        DocumentPermission.query.filter_by(document_id=document.id).delete()

        db.session.delete(document)
        db.session.commit()

    def create_document_permission_type_not_exist(self, document_permission_type: DocumentPermissionType):
        """Create document permission type to database if not exist
        """
        existing_type = db.session.query(DocumentPermissionType).filter_by(
            name=document_permission_type.name
        ).first()
        if existing_type is None:
            db.session.add(document_permission_type)
            db.session.commit()
            return document_permission_type
        else:
            return existing_type

    def create_document_permission(self, document_permission: DocumentPermission):
        """Create document permission to database
        """
        db.session.add(document_permission)
        db.session.commit()
        return document_permission

    def is_document_permission_type_exist(self, type_id):
        document_permission_type = DocumentPermissionType.query.filter_by(id=type_id).first()
        if document_permission_type:
            return True
        else:
            return False

    def get_document_mode(self, user: User, document: Document):
        if document.owner_id == user.id:
            return 2
        document_permission = DocumentPermission.query.\
            filter_by(user_id=user.id, document_id=document.id)\
            .first()
        if document_permission:
            return document_permission.document_permission_type_id
        else:
            return None
