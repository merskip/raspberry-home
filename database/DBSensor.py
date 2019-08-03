from sqlalchemy import Column, Integer, String, Table, ForeignKey
from sqlalchemy.orm import relationship

from database import Base
from database.DBCharacteristic import DBCharacteristic
from platform.sensor import Sensor


class DBSensor(Base):
    __tablename__ = 'sensors'

    id = Column(Integer, primary_key=True)
    name = Column(String(64))
    class_name = Column(String(64))

    characteristics = relationship("DBCharacteristic", secondary=Table(
        'sensors_to_characteristics', Base.metadata,
        Column('sensor_id', Integer, ForeignKey('sensors.id')),
        Column('characteristic_id', Integer, ForeignKey('characteristics.id'))
    ))

    @staticmethod
    def create(s: Sensor):
        characteristics = list(map(lambda c: DBCharacteristic.create(c), s.get_characteristics()))
        return DBSensor(id=s.id, name=s.name, class_name=s.__class__.__name__, characteristics=characteristics)
