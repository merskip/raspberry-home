from sqlalchemy import Column, Integer, ForeignKey, Float, DateTime
from sqlalchemy.orm import relationship

from database import Base
from database.DBCharacteristic import DBCharacteristic
from platform.measurement import Measurement


class DBMeasurement(Base):
    __tablename__ = 'measurements'
    __table_args__ = {'sqlite_autoincrement': True}

    id = Column(Integer, primary_key=True, nullable=False)
    sensor_id = Column(Integer, ForeignKey('sensors.id'), nullable=False)
    sensor = relationship("DBSensor")
    characteristic_id = Column(Integer, ForeignKey('characteristics.id'), nullable=False)
    characteristic = relationship("DBCharacteristic")
    value = Column(Float, nullable=False)
    time_start = Column(DateTime, nullable=False)
    time_end = Column(DateTime, nullable=False)

    @staticmethod
    def create(m: Measurement):
        db_characteristic = DBCharacteristic.create(m.sensor, m.characteristic)
        return DBMeasurement(sensor_id=m.sensor.id, characteristic_id=db_characteristic.id, value=m.value,
                             time_start=m.time_start, time_end=m.time_end)
