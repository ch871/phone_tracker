from returns.maybe import Maybe

from app.db.database import driver
from app.db.models import Device, Location


def create_device_repo(device: Device, location: Location):
    with driver.session() as session:
        query = """
        CREATE (d:Device { id: $id,
           name: $name,
           brand: $brand,
           model: $model,
           os: $os}), (l:Location{
               latitude: $latitude,
               longitude: $longitude,
               altitude_meters: $altitude_meters,
               accuracy_meters: $accuracy_meters})
            merge (d)-[:IS_IN]->(l)
            return d,l
        """
        params = {
            device.name,
            device.os,
            device.id,
            device.model,
            device.brand,
            location.latitude,
            location.longitude,
            location.accuracy_meters,
            location.altitude_meters
        }
        res = session.run(query, params).single()
        print(res)
        return (Maybe.from_optional(res.get('d'))
                .map(lambda d: dict(d)))
