from sqlalchemy import Column, Integer, ForeignKey, Float, DateTime
from sqlalchemy.orm import relationship

from database import Base
from platform.measurement import Measurement


class DBMeasurement(Base):
    __tablename__ = 'measurements'
    __table_args__ = {'sqlite_autoincrement': True}

    id = Column(Integer, primary_key=True)
    sensor_id = Column(Integer, ForeignKey('sensors.id'))
    sensor = relationship("DBSensor")
    characteristic_id = Column(Integer, ForeignKey('characteristics.id'))
    characteristic = relationship("DBCharacteristic")
    value = Column(Float)
    time_start = Column(DateTime)
    time_end = Column(DateTime)

    @staticmethod
    def create(m: Measurement):
        return DBMeasurement(sensor_id=m.sensor.id, characteristic_id=m.characteristic.id, value=m.value,
                             time_start=m.time_start, time_end=m.time_end)
