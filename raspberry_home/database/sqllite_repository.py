import hashlib
import sqlite3
from functools import reduce

from typing import List, Set

from raspberry_home.logger import Logger
from raspberry_home.platform.characteristic import Characteristic
from raspberry_home.platform.measurement import Measurement
from raspberry_home.platform.measurements_scheduler import MeasurementsListener
from raspberry_home.platform.sensor import Sensor


class SqliteRepository(MeasurementsListener):
    logger = Logger("SqliteRepository")

    def __init__(self, filename: str):
        self.logger.info("Using SQLite database: %s" % filename)
        self.connection = sqlite3.connect(filename, check_same_thread=False)
        self.connection.set_trace_callback(lambda sql: self.logger.verbose("Executing SQL: %s" % sql))
        self._create_tables()

    def _create_tables(self):
        self.connection.execute("""
            create table if not exists `sensors` (
                `sensor_id` int not null constraint `sensors_pk` primary key,
                `name` text not null,
                `class_name` text not null,
                `flags` text)""")

        self.connection.execute("""
            create table if not exists `characteristics` (
                `characteristic_id` text not null constraint `characteristics_pk` primary key,
                'sensor_id' int not null,
                `name` text not null,
                `type` text not null ,
                `unit` text,
                `min_value` float,
                `max_value` float,
                `accuracy` float,
                foreign key(sensor_id) references sensors(sensor_id))""")

        self.connection.commit()

    def update(self, sensors: List[Sensor]):
        self.logger.debug("Updating sensors and characteristics...")
        for sensor in sensors:
            self.connection.execute("replace into `sensors` values (?, ?, ?, ?)", [
                sensor.id,
                sensor.name,
                sensor.__class__.__name__,
                _sensor_flags(sensor)
            ])
            for characteristic in sensor.get_characteristics():
                self.connection.execute("replace into `characteristics` values (?, ?, ?, ?, ?, ?, ?, ?)", [
                    _generate_id(sensor, characteristic),
                    sensor.id,
                    characteristic.name,
                    characteristic.type.__class__.__name__,
                    characteristic.unit,
                    characteristic.min_value,
                    characteristic.max_value,
                    characteristic.accuracy
                ])

        self.connection.commit()

    def on_measurements(self, measurements: List[Measurement]):
        pass


def _sensor_flags(sensor: Sensor) -> str:
    return None if not sensor.flags else ",".join(sensor.flags)


def _generate_id(sensor: Sensor, characteristic: Characteristic) -> str:
    characteristics = list(filter(lambda c: c.type == characteristic.type, sensor.get_characteristics()))
    index = characteristics.index(characteristic)
    id_str = (str(sensor.id) + "." + str(index)).encode()
    return hashlib.sha256(id_str).hexdigest()
