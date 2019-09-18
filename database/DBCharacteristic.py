import hashlib

from sqlalchemy import Column, String, Float, Integer, ForeignKey
from sqlalchemy.orm import relationship

from database import Base
from platform.characteristic import Characteristic
from platform.sensor import Sensor


class DBCharacteristic(Base):
    __tablename__ = 'characteristics'

    id = Column(String(64), primary_key=True, nullable=False)
    name = Column(String(64), nullable=False)
    type = Column(String(32), nullable=False)
    unit = Column(String(16), nullable=True)
    min_value = Column(Float, nullable=True)
    max_value = Column(Float, nullable=True)
    accuracy = Column(Float, nullable=True)
    last_measurement_id = Column(Integer, ForeignKey('measurements.id'), nullable=True)
    last_measurement = relationship("DBMeasurement", foreign_keys=[last_measurement_id])

    @staticmethod
    def create(s: Sensor, c: Characteristic):
        id = DBCharacteristic._generate_id(s, c)
        return DBCharacteristic(id=id, name=c.name, type=c.type.__name__, unit=c.unit,
                                min_value=c.min_value, max_value=c.max_value,
                                accuracy=c.accuracy)

    @staticmethod
    def _generate_id(sensor: Sensor, characteristic: Characteristic):
        characteristics = list(filter(lambda c: c.type == characteristic.type, sensor.get_characteristics()))
        index = characteristics.index(characteristic)
        id_str = (str(sensor.id) + "." + str(index)).encode()
        return hashlib.sha256(id_str).hexdigest()
