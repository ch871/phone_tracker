import json

from app.db.models import Device, Location, Interaction


def split_data_to_models(data: json):
    devices = [Device(name=device["name"],
                      brand=device["brand"],
                      model=device["model"],
                      os=device["os"],
                      id=device["id"]) for device in data["devices"]]
    print(data["devices"])
    locations = [Location(latitude=device["location"]["latitude"],
                          longitude=device["location"]["longitude"],
                          altitude_meters=device["location"]["altitude_meters"],
                          accuracy_meters=device["location"]["accuracy_meters"]) for device in data["devices"]]
    interaction = [Interaction(**data["interaction"]) for interaction in data]
    return {"devices": devices,
            "locations": locations,
            "interaction": interaction}
