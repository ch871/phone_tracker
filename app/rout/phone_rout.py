from flask import Blueprint, request, jsonify
from app.repository.Interaction_repo import create_interaction_repo, get_connection_by_method_repo, \
    get_connection_stronger_then_repo, get_sum_connections_to_repo, check_if_too_connected_repo
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


@phone_blueprint.route("/connection/<method>", methods=['GET'])
def get_connection_by_method(method):
    res = get_connection_by_method_repo(method)
    try:
        return jsonify({"res": res}), 200
    except Exception as e:
        print(str(e))
        return jsonify({}), 404


@phone_blueprint.route("/relation_stronger_then/<int: streng_num>", methods=['GET'])
def get_connection_stronger_then(streng_num):
    res = get_connection_stronger_then_repo(streng_num)
    try:
        return jsonify({"res": res}), 200
    except Exception as e:
        print(str(e))
        return jsonify({}), 404


@phone_blueprint.route("/all_connected_to/<device_id>", methods=['GET'])
def get_sum_connections_to(device_id):
    res = get_sum_connections_to_repo(device_id)
    try:
        return jsonify({"res": res}), 200
    except Exception as e:
        print(str(e))
        return jsonify({}), 404


@phone_blueprint.route("/if_connect", methods=['POST'])
def check_if_too_connected():
    bool_res = check_if_too_connected_repo(request.json)
    if bool_res:
        res = "found connection"
    else:
        res = "not found connection"
    try:
        return jsonify({"res": res}), 200
    except Exception as e:
        print(str(e))
        return jsonify({}), 404


@phone_blueprint.route("/last_connection/<device_id>", methods=['GET'])
def get_last_connection(device_id):
    res = get_last_connection_repo(device_id)
    try:
        return jsonify({"res": res}), 200
    except Exception as e:
        print(str(e))
        return jsonify({}), 404