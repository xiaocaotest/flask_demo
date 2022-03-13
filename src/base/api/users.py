from flask import Blueprint
from flask import request
from flask import url_for, render_template_string
from src.base.utils.responses import response_with
from src.base.utils import responses as resp
from src.base.models.users import User, UserSchema
from flask_jwt_extended import create_access_token

user_routes = Blueprint("user_routes", __name__)


@user_routes.route('/', methods=['POST'])
def create_user():
    try:
        data = request.get_json()
        data['password'] = User.generate_hash(data['password'])
        user_schmea = UserSchema()
        user = user_schmea.load(data)
        user_schmea.dump(User(**user).create())
        return response_with(resp.SUCCESS_201)
    except Exception as e:
        print(e)
        return response_with(resp.INVALID_INPUT_422)


@user_routes.route('/login', methods=['POST'])
def authenticate_user():
    try:
        data = request.get_json()
        current_user = User.find_by_username(data['username'])
        if not current_user:
            return response_with(resp.SERVER_ERROR_404)
        if User.verify_hash(data['password'], current_user.password):
            access_token = create_access_token(identity=data['username'])
            return response_with(resp.SUCCESS_201, value={'message': f'Logged in as {current_user.username}',
                                                          "access_token": access_token})
        else:
            return response_with(resp.UNAUTHORIZED_401)
    except Exception as e:
        print(e)
        return response_with(resp.INVALID_INPUT_422)