from flask import Blueprint
from flask import request
from flask_jwt_extended import jwt_required

from src.base.utils.responses import response_with
from src.base.utils import responses as resp
from src.base.models.authors import Author, AuthorSchema

author_routes = Blueprint("author_routes", __name__)


@author_routes.route('/', methods=['POST'])
@jwt_required()
def create_author():
    try:
        json = request.get_json()
        author_schema = AuthorSchema()
        data = author_schema.load(json)
        author = Author(**data).create()
        result = author_schema.dump(author)
        return response_with(resp.SUCCESS_201, value={"author": result})
    except Exception as e:
        print(e)
        return response_with(resp.INVALID_INPUT_422)


@author_routes.route('/', methods=['GET'])
def get_author_list():
    fetched = Author.query.all()
    author_schema = AuthorSchema(many=True, only=['first_name',
                                                  'last_name',
                                                  'id'])
    authors = author_schema.dump(fetched)
    return response_with(resp.SUCCESS_200, value={"authors": authors})


@author_routes.route('/<int:author_id>', methods=['GET'])
def get_author_detail(author_id):
    fetched = Author.query.get_or_404(author_id)
    author_schema = AuthorSchema()
    author = author_schema.dump(fetched)
    return response_with(resp.SUCCESS_200, value={"author": author})


@author_routes.route('/<int:id>', methods=['PUT'])
def update_author_detail(id):
    data = request.get_json()
    author = Author(**data).put(id)
    author_schema = AuthorSchema()
    author = author_schema.dump(author)
    return response_with(resp.SUCCESS_200, value={"author": author})


@author_routes.route('/<int:id>', methods=['PATCH'])
def modify_author_detail(id):
    data = request.get_json()
    author = Author(**data).patch(id)
    author_schema = AuthorSchema()
    author = author_schema.dump(author)
    return response_with(resp.SUCCESS_200, value={"author": author})


@author_routes.route('/<int:id>', methods=['DELETE'])
def delete_author(id):
    Author().delete(id)
    return response_with(resp.SUCCESS_204)
