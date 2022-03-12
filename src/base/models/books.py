from src.base.utils.database import db
from marshmallow import Schema, fields


class Book(db.Model):
    __talbename__ = 'books'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(50))
    year = db.Column(db.Integer)
    author_id = db.Column(db.Integer, db.ForeignKey('authors.id'))

    def __init__(self, title, year, author_id=None):
        self.title = title
        self.year = year
        self.author_id = author_id

    def create(self):
        db.session.add(self)
        db.session.commit()
        return self


class BookSchema(Schema):
    class Meta(Schema.Meta):
        model = Book
        sqla_session = db.session

    id = fields.Number(dump_only=True)
    title = fields.String(required=True)
    year = fields.Integer(required=True)
    author_id = fields.Integer()