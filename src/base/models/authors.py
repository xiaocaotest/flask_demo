from src.base.utils.database import db
from marshmallow import Schema, fields
from src.base.models.books import BookSchema


class Author(db.Model):
    __tablename__ = 'authors'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    first_name = db.Column(db.String(20))
    last_name = db.Column(db.String(20))
    created = db.Column(db.DateTime, server_default=db.func.now())
    books = db.relationship('Book', backref='Author',  cascade="all, delete-orphan")

    def __init__(self, first_name, last_name, books=None):
        if books is None:
            books = []
        self.first_name = first_name
        self.last_name = last_name
        self.books = books

    def create(self):
        db.session.add(self)
        db.session.commit()
        return self


class AuthorSchema(Schema):
    class Meta(Schema.Meta):
        model = Author
        sqla_session = db.session

    id = fields.Number(dump_only=True)
    first_name = fields.String(required=True)
    last_name = fields.String(required=True)
    created = fields.String(dump_only=True)
    books = fields.Nested(BookSchema, many=True, only=['title', 'year', 'id'])
