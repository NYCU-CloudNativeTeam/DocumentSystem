from marshmallow import Schema, fields


class MessageSchema(Schema):
    """Schema for validating message data.
    """
    recipient = fields.String(required = True)
    title = fields.String(required = True)
    content = fields.String(required = True)
    notification_type = fields.String(load_default = "email")