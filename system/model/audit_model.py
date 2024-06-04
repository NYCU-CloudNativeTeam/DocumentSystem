from datetime import datetime

from .base_model import db

class Audit(db.Model):
    __tablename__ = 'audit'
    id = db.Column(db.Integer, primary_key=True)
    uid = db.Column(db.String(50), unique=True, nullable=False)
    document_id = db.Column(db.Integer, db.ForeignKey('document.id'), nullable=False)
    auditor_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    audit_status_id = db.Column(db.Integer, db.ForeignKey('audit_status.id'), nullable=False)
    rejected_reason = db.Column(db.Text, nullable=True)
    created_date = db.Column(db.DateTime, default=datetime.utcnow)
    updated_date = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def to_dict(self) -> dict:
        # Convert the Audit object to a dictionary.
        return {
            'id': self.id,
            'uid': self.uid,
            'document_id': self.document_id,
            'auditor_id': self.auditor_id,
            'audit_status_id': self.audit_status_id,
            'rejected_reason': self.rejected_reason,
            'created_date': self.created_date,
            'updated_date': self.updated_date
        }

    auditor = db.relationship('User', backref='audits')
    document = db.relationship('Document', backref='audits')

class AuditStatus(db.Model):
    __tablename__ = 'audit_status'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    audit_status_value = db.Column(db.Integer)
    created_date = db.Column(db.DateTime, default=datetime.utcnow)
    updated_date = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
