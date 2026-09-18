import os

from dotenv import load_dotenv
from flask import Flask, jsonify
from flask_jwt_extended import JWTManager
from flask_migrate import Migrate
from flask_smorest import Api
from sqlalchemy.exc import SQLAlchemyError

from py_rest_api.block_list import BLOCKLIST
from py_rest_api.db import db

load_dotenv()

from py_rest_api.resources.item import blp as item_blp
from py_rest_api.resources.store import blp as store_blp
from py_rest_api.resources.tag import blp as tag_blp
from py_rest_api.resources.user import blp as user_blp


def create_app(db_url=None):

    app = Flask(__name__)
    app.config["PROPAGATE_EXCEPTIONS"] = True
    app.config["API_TITLE"] = "Stores REST API"
    app.config["API_VERSION"] = "v1"
    app.config["OPENAPI_VERSION"] = "3.0.3"
    app.config["OPENAPI_URL_PREFIX"] = "/"
    app.config["OPENAPI_SWAGGER_UI_PATH"] = "/swagger-ui"
    app.config["OPENAPI_SWAGGER_UI_URL"] = (
        "https://cdn.jsdelivr.net/npm/swagger-ui-dist/"
    )
    app.config["SQLALCHEMY_DATABASE_URI"] = db_url or os.getenv(
        "DATABASE_URI", "sqlite:///data.db"
    )
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    try:
        db.init_app(app)
        migrate = Migrate(app, db)
    except SQLAlchemyError as e:
        print(e)

    with app.app_context():
        db.create_all()

    api = Api(app)
    api.spec.components.security_scheme(
        "bearerAuth",
        {"type": "http", "scheme": "bearer", "bearerFormat": "JWT"},
    )

    app.config["JWT_SECRET_KEY"] = "58216975469707516585755993795747836917"
    jwt = JWTManager(app)

    @jwt.token_in_blocklist_loader
    def check_if_token_in_blocklist(jwt_header, jwt_payload):
        return jwt_payload["jti"] in BLOCKLIST

    @jwt.revoked_token_loader
    def revoked_token_callback(jwt_header, jwt_payload):
        return (
            jsonify(
                {"description": "The token has been revoked.", "error": "token_revoked"}
            ),
            401,
        )

    @jwt.needs_fresh_token_loader
    def needs_fresh_token_callback(jwt_header, jwt_payload):
        return (
            jsonify(
                {
                    "description": "The Token is not fresh.",
                    "error": "fresh_token_required",
                }
            ),
            401,
        )

    @jwt.expired_token_loader
    def expired_token_callback(jwt_header, jwt_payload):
        return (
            jsonify({"message": "The token has expired.", "error": "token_expired"}),
            401,
        )

    @jwt.invalid_token_loader
    def invalid_token_callback(error):
        return (
            jsonify(
                {"message": "Signature verification failed.", "error": "invalid_token"}
            ),
            401,
        )

    @jwt.unauthorized_loader
    def unauthorized_callback(error):
        return (
            jsonify(
                {
                    "message": "Request does not contain an access token.",
                    "error": "authorization_required",
                }
            ),
            401,
        )

    api.register_blueprint(store_blp)
    api.register_blueprint(item_blp)
    api.register_blueprint(tag_blp)
    api.register_blueprint(user_blp)

    return app


def main():
    create_app().run()
