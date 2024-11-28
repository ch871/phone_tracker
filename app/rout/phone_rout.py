from flask import Blueprint, request, jsonify

from app.repository.device_repo import create_device_repo
from app.service.split_data import split_data_to_models

phone_blueprint = Blueprint("phone", __name__)


@phone_blueprint.route("", methods=['POST'])
def get_interaction():
    split_data = split_data_to_models(request.json)
    create_device_repo(split_data["devices"], split_data["locations"])
    print(request.json)
    return jsonify({}), 200
