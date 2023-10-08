from marshmallow import Schema, fields, validate


class UserSchema(Schema):
    id = fields.Integer(dump_only=True)
    username = fields.String(required=True, validate=validate.Length(min=1))
    email = fields.String(required=True)
    password = fields.String(required=True, validate=validate.Length(min=8))

class CreatureSchema(Schema):
    id = fields.Integer(dump_only=True)
    bug_name = fields.String(required=True)
    image = fields.String()
    bug_description = fields.String(required=True)


class BiteTreatmentSchema(Schema):
    id = fields.Integer(dump_only=True)
    treatment_plan = fields.String()



class BugBiteSchema(Schema):
    id = fields.Integer(dump_only=True)
    bite_description = fields.String(required=True, validate=validate.Length(min=10))
    symptoms = fields.String()
    severity_of_bite = fields.String()
    treatment_plan_id = fields.Integer(required=True)
    creatures = fields.List(fields.String())