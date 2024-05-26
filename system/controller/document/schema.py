from marshmallow import Schema, fields

class NewDocumentSchema(Schema):
    """Schema for validating new document data."""
    name = fields.String(required=True)
    owner_id = fields.Integer(required=True)
    document_status_id = fields.Integer(required=True)

class UpdateDocumentSchema(Schema):
    """Schema for validating updated document data."""
    body = fields.String(required=True)
    comments = fields.List(fields.Dict(), required=True)
