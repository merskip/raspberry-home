from sqlalchemy import Column, Integer, ForeignKey, Float, BigInteger, String
from sqlalchemy.orm import relationship

from database import Base
from database.DBCharacteristic import DBCharacteristic
from platform.measurement import Measurement
from platform.sensor import Sensor


class DBMeasurement(Base):
    __tablename__ = 'measurements'
    __table_args__ = {'sqlite_autoincrement': True}

    id = Column(Integer, primary_key=True, nullable=False)
    sensor_id = Column(Integer, ForeignKey('sensors.id'), nullable=False)
    sensor = relationship("DBSensor")
    characteristic_id = Column(String(64), ForeignKey('characteristics.id'), nullable=False)
    characteristic = relationship("DBCharacteristic")
    value = Column(Float, nullable=False)
    formatted_value = Column(String(32), nullable=False)
    time_start = Column(BigInteger, nullable=False)
    time_end = Column(BigInteger, nullable=False)

    @staticmethod
    def create(m: Measurement):
        db_characteristic = DBCharacteristic.create(m.sensor, m.characteristic)
        return DBMeasurement(sensor_id=m.sensor.id, characteristic_id=db_characteristic.id,
                             value=m.value, formatted_value=Sensor.formatted_value(m.characteristic, m.value),
                             time_start=m.time_start.timestamp() * 1e6,
                             time_end=m.time_end.timestamp() * 1e6)
