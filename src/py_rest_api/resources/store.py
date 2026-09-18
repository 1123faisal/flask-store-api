from flask.views import MethodView
from flask_jwt_extended import jwt_required
from flask_smorest import Blueprint, abort
from sqlalchemy.exc import IntegrityError, SQLAlchemyError

from py_rest_api.db import db
from py_rest_api.models.store import StoreModel
from py_rest_api.schemas import (
    PlainStoreSchema,
    StoreListSchema,
    StoreSchema,
    StoreUpdateSchema,
)

blp = Blueprint("stores", __name__, description="Operations on stores")


@blp.route("/store/<int:store_id>")
class Store(MethodView):
    @jwt_required()
    @blp.doc(security=[{"bearerAuth": []}])
    @blp.response(200, PlainStoreSchema)
    def get(self, store_id):
        store = StoreModel.query.get_or_404(store_id)
        return store

    @jwt_required()
    @blp.doc(security=[{"bearerAuth": []}])
    @blp.arguments(StoreUpdateSchema)
    @blp.response(200, PlainStoreSchema)
    def put(self, store_data, store_id):
        store = StoreModel.query.get(store_id)
        if store:
            store.name = store_data["name"]
        else:
            store = StoreModel(id=store_id, **store_data)

        db.session.add(store)
        db.session.commit()
        return store

    @jwt_required()
    @blp.doc(security=[{"bearerAuth": []}])
    def delete(self, store_id):
        store = StoreModel.query.get_or_404(store_id)
        db.session.delete(store)
        db.session.commit()
        return {"message": f"Store {store.id} Deleted."}


@blp.route("/store")
class StoreList(MethodView):
    @jwt_required()
    @blp.doc(security=[{"bearerAuth": []}])
    @blp.response(200, StoreListSchema)
    def get(self):
        stores = StoreModel.query.all()
        return {"stores": stores}

    @jwt_required()
    @blp.doc(security=[{"bearerAuth": []}])
    @blp.arguments(StoreSchema)
    @blp.response(201, StoreSchema)
    def post(self, store_data):
        store = StoreModel(**store_data)
        try:
            db.session.add(store)
            db.session.commit()
        except IntegrityError:
            abort(400, message="A Store with that name already exists.")
        except SQLAlchemyError:
            abort(500, message="An error occurred while inserting the store.")
        return store
