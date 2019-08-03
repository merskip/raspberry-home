from sqlalchemy import Column, String, Integer

from database import Base
from platform.characteristic import Characteristic


class DBCharacteristic(Base):
    __tablename__ = 'characteristics'

    id = Column(Integer, primary_key=True)
    name = Column(String(64))
    type = Column(String(32))
    unit = Column(String(16))

    @staticmethod
    def create(c: Characteristic):
        return DBCharacteristic(id=c.id, name=c.name, type=c.type.__name__, unit=c.unit)
