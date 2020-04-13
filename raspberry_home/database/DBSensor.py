from sqlalchemy import Column, Integer, String, Table, ForeignKey
from sqlalchemy.orm import relationship

from raspberry_home.database import Base
from raspberry_home.database.DBCharacteristic import DBCharacteristic
from raspberry_home.platform.sensor import Sensor


class DBSensor(Base):
    __tablename__ = 'sensors'

    id = Column(Integer, primary_key=True, nullable=False)
    name = Column(String(64), nullable=False)
    class_name = Column(String(64), nullable=False)
    characteristics = relationship("DBCharacteristic", secondary=Table(
        'sensors_to_characteristics', Base.metadata,
        Column('sensor_id', Integer, ForeignKey('sensors.id'), nullable=False),
        Column('characteristic_id', String(64), ForeignKey('characteristics.id'), nullable=False)
    ))
    flags = Column(String(128), nullable=True)

    @staticmethod
    def create(s: Sensor):
        characteristics = list(map(lambda c: DBCharacteristic.create(s, c), s.get_characteristics()))
        return DBSensor(id=s.id, name=s.name, class_name=s.__class__.__name__, characteristics=characteristics,
                        flags=DBSensor._convert_flags(s.flags))

    @staticmethod
    def _convert_flags(flags: str):
        return None if not flags else ",".join(flags)
