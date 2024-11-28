import json


def split_data_to_models(data: json):
    devices = [{"name": device["name"],
                "brand": device["brand"],
                "model": device["model"],
                "os": device["os"],
                "id": device["id"]} for device in data["devices"]]
    locations = [{"latitude": device["location"]["latitude"],
                  "longitude": device["location"]["longitude"],
                  "altitude_meters": device["location"]["altitude_meters"],
                  "accuracy_meters": device["location"]["accuracy_meters"]} for device in data["devices"]]
    interaction = data["interaction"]
    return {"devices": devices,
            "locations": locations,
            "interaction": interaction}
