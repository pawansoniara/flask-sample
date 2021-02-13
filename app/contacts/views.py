from http import HTTPStatus

from flask import Blueprint, jsonify
from flask import request

from app.contacts.models import Contact
from app.contacts.schemas import ContactSchema
from app.database import db


contacts_api = Blueprint('contacts_api', __name__)


@contacts_api.route('/', methods=["GET"])
@contacts_api.route('/<string:username>/', methods=["GET"])
def retrieve_contacts(username=None):
    if username:
        contact = Contact.query.filter_by(username=username).first_or_404()
        schema = ContactSchema().dump(contact)
        return jsonify(schema.data), HTTPStatus.OK

    contacts = Contact.query.all()
    schema = ContactSchema(many=True).dump(contacts)
    return jsonify(schema.data), HTTPStatus.OK


@contacts_api.route('/', methods=["POST"])
def create_contact():
    data = request.get_json()
    schema = ContactSchema()

    validated_data, errors = schema.load(data)

    if errors:
        return jsonify(errors), HTTPStatus.BAD_REQUEST
    return jsonify(schema.dump(schema.instance).data), HTTPStatus.CREATED


@contacts_api.route('/<string:username>/', methods=["PUT", "PATCH"])
def update_contact(username):
    contact = Contact.query.filter_by(username=username).first_or_404()

    data = request.get_json()

    schema = ContactSchema()
    if request.method == 'PATCH':
        errors = schema.validate(data, partial=True)
    else:
        errors = schema.validate(data)

    if errors:
        return jsonify(errors), HTTPStatus.BAD_REQUEST

    schema.update_contact(contact, data)
    updated_contact = Contact.query.filter_by(id=contact.id).first()
    return jsonify(ContactSchema().dump(updated_contact).data), HTTPStatus.ACCEPTED


@contacts_api.route('/<string:username>/', methods=["DELETE"])
def delete_contact(username):
    contact = Contact.query.filter_by(username=username).first_or_404()
    db.session.delete(contact)
    db.session.commit()
    return '', HTTPStatus.NO_CONTENT
