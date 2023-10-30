from mongoengine import StringField, Document, IntField


class Process(Document):
    name = StringField()
    description = StringField()


class Risk(Document):
    process_id = StringField()
    name = StringField()
    importance = IntField()
    description = StringField()
