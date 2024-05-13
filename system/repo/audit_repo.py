from typing import List

from model.audit_model import Audit
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