from flask.views import MethodView
from flask_jwt_extended import jwt_required
from flask_smorest import Blueprint, abort
from sqlalchemy import delete
from sqlalchemy.exc import SQLAlchemyError

from py_rest_api.db import db
from py_rest_api.models.item import ItemModel
from py_rest_api.schemas import (
    ItemListSchema,
    ItemSchema,
    ItemUpdateSchema,
)

blp = Blueprint("items", __name__, description="Operations on items")


@blp.route("/item/<int:item_id>")
class Item(MethodView):

    @jwt_required()
    @blp.doc(security=[{"bearerAuth": []}])
    @blp.response(200, ItemSchema)
    def get(self, item_id):
        return ItemModel.query.get_or_404(item_id)

    @jwt_required()
    @blp.doc(security=[{"bearerAuth": []}])
    @blp.arguments(ItemUpdateSchema)
    @blp.response(200, ItemSchema)
    def put(self, item_data, item_id):
        item = db.session.get(ItemModel, item_id)

        if item:
            item.name = item_data["name"]
            item.price = item_data["price"]
        else:
            item = ItemModel(id=item_id, **item_data)

        db.session.add(item)
        db.session.commit()
        return item

    @jwt_required()
    @blp.doc(security=[{"bearerAuth": []}])
    def delete(self, item_id):
        item = ItemModel.query.get_or_404(item_id)
        db.session.delete(item)
        db.session.commit()
        return {"message": f"Item {item.id} Deleted."}


@blp.route("/item")
class ItemList(MethodView):
    @jwt_required()
    @blp.doc(security=[{"bearerAuth": []}])
    @blp.response(200, ItemListSchema)
    def get(self):
        items = ItemModel.query.all()
        return {"items": items}

    @jwt_required()
    @blp.doc(security=[{"bearerAuth": []}])
    @blp.arguments(ItemSchema)
    @blp.response(201, ItemSchema)
    def post(self, item_data):
        item = ItemModel(**item_data)
        try:
            db.session.add(item)
            db.session.commit()
        except SQLAlchemyError:
            abort(500, message="An error occurred, while inserting the item.")

        return item
