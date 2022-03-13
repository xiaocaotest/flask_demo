from flask import Blueprint, request
from src.base.utils.responses import response_with
from src.base.utils import responses as resp
from src.base.models.books import Book, BookSchema

book_routes = Blueprint("book_routes", __name__)


@book_routes.route('/', methods=['POST'])
def create_book():
    try:
        data = request.get_json()
        book_schema = BookSchema()
        data = book_schema.load(data)
        book = Book(**data).create()
        result = book_schema.dump(book)
        return response_with(resp.SUCCESS_201, value={"book": result})
    except Exception as e:
        print(e)
    return response_with(resp.INVALID_INPUT_422)


@book_routes.route('/', methods=['GET'])
def get_book_list():
    fetched = Book.query.all()
    book_schema = BookSchema(many=True, only=['author_id', 'title', 'year'])
    books = book_schema.dump(fetched)
    return response_with(resp.SUCCESS_200, value={"books": books})


@book_routes.route('/<int:id>', methods=['GET'])
def get_book_detail(id):
    fetched = Book.query.get_or_404(id)
    book_schema = BookSchema()
    books = book_schema.dump(fetched)
    return response_with(resp.SUCCESS_200, value={"books": books})


@book_routes.route('/<int:id>', methods=['PUT'])
def update_book_detail(id):
    data = request.get_json()
    get_book = Book(**data).put(id)
    book_schema = BookSchema()
    book = book_schema.dump(get_book)
    return response_with(resp.SUCCESS_200, value={"book": book})


@book_routes.route('/<int:id>', methods=['PATCH'])
def modify_book_detail(id):
    data = request.get_json()
    get_book = Book(**data).patch(id)
    book_schema = BookSchema()
    book = book_schema.dump(get_book)
    return response_with(resp.SUCCESS_200, value={"book": book})


@book_routes.route('/<int:id>', methods=['DELETE'])
def delete_book(id):
    Book().delete(id)
    return response_with(resp.SUCCESS_204)
