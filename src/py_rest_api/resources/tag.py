from flask import abort
from flask.views import MethodView
from flask_jwt_extended import jwt_required
from flask_smorest import Blueprint
from sqlalchemy.exc import IntegrityError, SQLAlchemyError

from py_rest_api.db import db
from py_rest_api.models.item import ItemModel
from py_rest_api.models.item_tags import ItemTags
from py_rest_api.models.store import StoreModel
from py_rest_api.models.tag import TagModel
from py_rest_api.schemas import TagAndItemSchema, TagSchema

blp = Blueprint("tags", __name__, description="Operations on tags")


@blp.route("/store/<int:store_id>/tag")
class TagsInStore(MethodView):
    @jwt_required()
    @blp.doc(security=[{"bearerAuth": []}])
    @blp.response(200, TagSchema(many=True))
    def get(self, store_id):
        store = StoreModel.query.get_or_404(store_id)
        return store.tags.all()

    @jwt_required()
    @blp.doc(security=[{"bearerAuth": []}])
    @blp.arguments(TagSchema)
    @blp.response(201, TagSchema)
    def post(self, tag_data, store_id):
        if TagModel.query.filter(
            TagModel.store_id == store_id, TagModel.name == tag_data["name"]
        ).first():
            abort(400, message="A tag with that name is already exists.")

        tag = TagModel(**tag_data, store_id=store_id)
        try:
            db.session.add(tag)
            db.session.commit()
        except IntegrityError:
            abort(400, message="A Tag with same name already exists")
        except SQLAlchemyError as e:
            abort(500, message=str(e))

        return tag


@blp.route("/item/<int:item_id>/tag/<int:tag_id>")
class LinkTagsToItem(MethodView):
    @jwt_required()
    @blp.doc(security=[{"bearerAuth": []}])
    @blp.response(201, TagSchema)
    def post(self, item_id, tag_id):
        item = ItemModel.query.get_or_404(item_id)
        tag = TagModel.query.get_or_404(tag_id)

        if tag.store.id != item.store.id:
            abort(400, message="You can't link a store tag to another store")

        item.tags.append(tag)
        try:
            db.session.add(item)
            db.session.commit()
        except SQLAlchemyError:
            abort(500, message="An error occurred while linking tag with item.")

        return tag

    @jwt_required()
    @blp.doc(security=[{"bearerAuth": []}])
    @blp.response(200, TagAndItemSchema)
    def delete(self, item_id, tag_id):
        item = ItemModel.query.get_or_404(item_id)
        tag = TagModel.query.get_or_404(tag_id)

        item.tags.remove(tag)
        try:
            db.session.add(item)
            db.session.commit()
        except SQLAlchemyError:
            abort(500, message="An error occurred while un-linking tag with item.")

        return {"message": "item removed from tag", "item": item, "tag": tag}


@blp.route("/tag/<int:tag_id>")
class Tag(MethodView):
    @jwt_required()
    @blp.doc(security=[{"bearerAuth": []}])
    @blp.response(200, TagSchema)
    def get(self, tag_id):
        return TagModel.query.get_or_404(tag_id)


    @jwt_required()
    @blp.doc(security=[{"bearerAuth": []}])
    @blp.response(
        202,
        description="Deletes a tag if no item is tagged with it.",
        example={"message": "Tag Deleted."},
    )
    @blp.alt_response(404, description="Tag not found.")
    @blp.alt_response(
        400,
        description="Returned if the tag is assigned to one or more items. In this case, the tag not deleted.",
    )
    def delete(self, tag_id):
        tag = TagModel.query.get_or_404(tag_id)

        if not tag.items:
            db.session.delete(tag)
            db.session.commit()
            return {"message": "Tag deleted."}
        abort(
            400,
            "Could not delete tag. make sure tag is not associated with any items, then try again.",
        )
