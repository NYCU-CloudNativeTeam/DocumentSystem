from typing import List

from model.audit_model import Audit, AuditStatus
from model.base_model import db

class AuditRepository:
    """
    Repository class for accessing Audit data.
    """

    def get_all_audits(self, sort: str = 'created_date') -> List[Audit]:
        """Retrieve all audits with optional sorting."""
        return Audit.query.order_by(sort).all()

    def create_audit(self, audit: Audit) -> Audit:
        """Create a new audit record."""
        db.session.add(audit)
        db.session.commit()
        return audit
    
    def update_audit(self, audit: Audit) -> Audit:
        """Update an existing audit record."""
        db.session.commit()

    def create_audit_status(self, audit_status: AuditStatus) -> AuditStatus:
        """Create a new audit status record."""
        db.session.add(audit_status)
        db.session.commit()
        return audit_status
    
    def update_audit_status(self, audit_status: AuditStatus) -> AuditStatus:
        """Update an existing audit status record."""
        db.session.commit()

    def get_audit_by_document_id(self, document_uid: str) -> Audit:
        """Get audit record by document UID."""
        return Audit.query.filter_by(document_id=document_uid).first()

    def get_audit_status_by_audit_status_id(self, audit_status_uid: str) -> AuditStatus:
        """Get audit status by audit_status_id."""
        return AuditStatus.query.filter_by(id=audit_status_uid).first()
