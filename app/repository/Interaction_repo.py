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
