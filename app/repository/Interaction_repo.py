from returns.maybe import Maybe
from app.db.database import driver
from app.db.models import Interaction


def create_interaction_repo(interaction: Interaction):
    with driver.session() as session:
        query = """
        match (d1:Device{ id: $from_device}),(d2:Device{ id: $to_device})
        merge (d1) -[:CONNECTED{method: $method,
        bluetooth_version: $bluetooth_version,
        signal_strength_dbm: $signal_strength_dbm,
        distance_meters: $distance_meters,
        duration_seconds: $duration_seconds,
        timestamp: $timestamp}]->(d2)
        return d1,d2
        """
        params = {
            "method": interaction.method,
            "to_device": interaction.to_device,
            "timestamp": interaction.timestamp,
            "from_device": interaction.from_device,
            "bluetooth_version": interaction.bluetooth_version,
            "distance_meters": interaction.distance_meters,
            "duration_seconds": interaction.duration_seconds,
            "signal_strength_dbm": interaction.signal_strength_dbm
        }
        res = session.run(query, params).single()
        return (Maybe.from_optional(res.get("d"))
                .map(lambda d: dict(d)))


def get_connection_by_method_repo(method):
    with driver.session() as session:
        query = """
        match path =(d:Device) -[:CONNECTED{method: $method}]->(d1:Device) where not d = d1 return d,d1,length(path) as len
        """
        params = {
            "method": method
        }
        res = session.run(query, params).data()
        return res


def get_connection_stronger_then_repo(streng_num: int):
    with driver.session() as session:
        query = """
        match(d:Device) -[rel:CONNECTED]-> (d1:Device) where rel.signal_strength_dbm >=$streng_num return d,d1
        """
        params = {
            "streng_num": streng_num
        }
        res = session.run(query, params).data()
        return res


def get_sum_connections_to_repo(device_id):
    with driver.session() as session:
        query = """
        match(d:Device{id:$device_id}) <-- (d1:Device) 
        return count(d) as sum_connection
        """
        params = {
            "device_id": device_id
        }
        res = session.run(query, params).data()
        return res


def check_if_too_connected_repo(devices):
    with driver.session() as session:
        query = """
        match(d:Device{id: $from_device }) -[:CONNECTED]-> (d1:Device{id: $to_device })  return d,d1
        """
        params = {
            "from_device": devices["from_device"],
            "to_device": devices["to_device"]
        }

        res = session.run(query, params).single()
        return True if res else False


def get_last_connection_repo(device_id):
    with driver.session() as session:
        query = """
        match(d:Device{id: $device_id}) -[rel:CONNECTED]-> (d1:Device) 
        return d,d1 order by rel.timestamp  asc limit 1
        """
        params = {
            "device_id": device_id
        }
        res = session.run(query, params).data()
        return res
