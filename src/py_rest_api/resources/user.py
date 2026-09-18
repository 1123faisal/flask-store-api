from flask import abort
from flask.views import MethodView
from flask_jwt_extended import (
    create_access_token,
    create_refresh_token,
    get_jwt,
    get_jwt_identity,
    jwt_required,
)
from flask_smorest import Blueprint
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from werkzeug.security import check_password_hash, generate_password_hash


from py_rest_api.block_list import BLOCKLIST
from py_rest_api.db import db
from py_rest_api.models.user import UserModel
from py_rest_api.schemas import PlainUserSchema

blp = Blueprint("user", __name__, description="Operations on User")


@blp.route("/register")
class UserRegister(MethodView):
    @blp.arguments(PlainUserSchema)
    def post(self, user_data):
        user = UserModel(
            username=user_data["username"],
            password=generate_password_hash(user_data["password"]),
        )

        try:
            db.session.add(user)
            db.session.commit()
        except IntegrityError:
            abort(409, message="Same username already exists")
        except SQLAlchemyError as e:
            abort(500, message="An error occurred, while creating user")

        return {"message": "User created Successfully"}, 201


@blp.route("/login")
class UserLogin(MethodView):
    @blp.arguments(PlainUserSchema)
    def post(self, user_data):
        user = UserModel.query.filter(
            UserModel.username == user_data["username"]
        ).first()

        if user and check_password_hash(user.password, user_data["password"]):
            access_token = create_access_token(identity=str(user.id), fresh=True)
            refresh_token = create_refresh_token(identity=str(user.id))
            return {"access_token": access_token, "refresh_token": refresh_token}

        abort(401, message="Invalid Credentials.")


@blp.route("/refresh")
class TokenRefresh(MethodView):
    @jwt_required(refresh=True)
    def post(self):
        current_user = get_jwt_identity()
        new_token = create_access_token(identity=current_user, fresh=False)
        return {"access_token": new_token}


@blp.route("/logout")
class UserLogout(MethodView):
    @jwt_required()
    @blp.doc(security=[{"bearerAuth": []}])
    def post(self):
        jti = get_jwt().get("jti")
        BLOCKLIST.add(jti)
        return {"message": "Successfully Logout."}


@blp.route("/user/<int:user_id>")
class User(MethodView):
    @jwt_required()
    @blp.doc(security=[{"bearerAuth": []}])
    @blp.response(200, PlainUserSchema)
    def get(self, user_id):
        return UserModel.query.get_or_404(user_id)

    @jwt_required()
    @blp.doc(security=[{"bearerAuth": []}])
    @blp.response(200, example={"message": "User deleted."})
    def delete(self, user_id):
        user = UserModel.query.get_or_404(user_id)
        db.session.delete(user)
        db.session.commit()
        return {"message": "User deleted."}
