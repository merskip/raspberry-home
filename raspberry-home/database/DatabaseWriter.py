from typing import List

from sqlalchemy import engine
from sqlalchemy.orm import sessionmaker

from database import Base
from database.DBCharacteristic import DBCharacteristic
from database.DBMeasurement import DBMeasurement
from database.DBSensor import DBSensor
from platform.measurement import Measurement
from platform.measurements_scheduler import MeasurementsListener
from platform.platform import Platform


class DatabaseWriter(MeasurementsListener):

    def __init__(self, engine: engine, platform: Platform):
        self.session = sessionmaker(bind=engine)()
        Base.metadata.create_all(engine)
        self._insert_sensors(platform)

    def _insert_sensors(self, platform: Platform):
        db_sensors = list(map(lambda s: DBSensor.create(s), platform.get_sensors()))
        for db_sensor in db_sensors:
            self.session.merge(db_sensor)
        self.session.commit()

    def on_measurements(self, measurements: List[Measurement]):
        for measurement in measurements:
            if not measurement.sensor.is_storable():
                continue

            db_measurement = DBMeasurement.create(measurement)

            self.session.add(db_measurement)
            self.session.flush()

            self.session.query(DBCharacteristic)\
                .filter_by(id=db_measurement.characteristic_id)\
                .update(dict(last_measurement_id=db_measurement.id))

        self.session.commit()