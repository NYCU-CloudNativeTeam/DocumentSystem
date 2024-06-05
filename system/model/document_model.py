from datetime import datetime
from .base_model import db

class Document(db.Model):
    __tablename__ = 'document'
    id = db.Column(db.Integer, primary_key=True)
    uid = db.Column(db.String(50), unique=True, nullable=False)
    name = db.Column(db.String(100), nullable=False)
    body = db.Column(db.Text, nullable=True)
    owner_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    lock_session = db.Column(db.String(50), nullable=True)
    document_status_id = db.Column(db.Integer, db.ForeignKey('document_status.id'), nullable=False)
    created_date = db.Column(db.DateTime, default=datetime.utcnow)
    updated_date = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def to_dict(self) -> dict:
        return {
            'uid': self.uid,
            'name': self.name,
            'body': self.body,
            'owner_id': self.owner_id,
            'lock_session': self.lock_session,
            'document_status_id': self.document_status_id,
            'created_date': self.created_date,
            'updated_date': self.updated_date,
        }

class DocumentStatus(db.Model):
    __tablename__ = 'document_status'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    created_date = db.Column(db.DateTime, default=datetime.utcnow)
    updated_date = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class DocumentComment(db.Model):
    __tablename__ = 'document_comment'
    id = db.Column(db.Integer, primary_key=True)
    inline_id = db.Column(db.String(50), nullable=True)
    document_id = db.Column(db.Integer, db.ForeignKey('document.id'), nullable=False)
    text = db.Column(db.Text, nullable=False)
    commenter_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    created_by_auditor = db.Column(db.Boolean, default=False)
    created_date = db.Column(db.DateTime, default=datetime.utcnow)
    updated_date = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def to_dict(self) -> dict:
        return {
            'inlineId': self.inline_id,
            'text': self.text,
            'commenter': {
                'name': self.commenter.name,
            },
            'created_by_auditor': self.created_by_auditor,
            'created_date': self.created_date,
            'updated_date': self.updated_date
        }

class DocumentPermission(db.Model):
    __tablename__ = 'document_permission'
    id = db.Column(db.Integer, primary_key=True)
    document_id = db.Column(db.Integer, db.ForeignKey('document.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    document_permission_type_id = db.Column(db.Integer, db.ForeignKey('document_permission_type.id'), nullable=False)
    created_date = db.Column(db.DateTime, default=datetime.utcnow)
    updated_date = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    document = db.relationship('Document', backref='permissions')

class DocumentPermissionType(db.Model):
    __tablename__ = 'document_permission_type'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    created_date = db.Column(db.DateTime, default=datetime.utcnow)
    updated_date = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
