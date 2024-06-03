from marshmallow import Schema, fields


class NewAuditSchema(Schema):
    """Schema for validating message data.
    """
    documentUid = fields.String(required = True)
    auditorUsername = fields.String(required = True)