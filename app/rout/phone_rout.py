from flask import Blueprint, request, jsonify

from app.db.models import Device, Location
from app.repository.Interaction_repo import create_interaction_repo
from app.repository.device_repo import create_device_repo
from app.service.split_data import split_data_to_models

phone_blueprint = Blueprint("phone", __name__)


@phone_blueprint.route("", methods=['POST'])
def get_interaction():
    split_data = split_data_to_models(request.json)

    for index, device in enumerate(split_data["devices"]):
        create_device_repo(device, split_data["locations"][index])
    create_interaction_repo(split_data["interaction"])
    print(request.json)
    return jsonify({}), 200
