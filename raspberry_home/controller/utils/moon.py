import math
from datetime import datetime
from decimal import Decimal
from enum import Enum


class MoonPhase(Enum):
    NEW_MOON = 0
    WAXING_CRESCENT = 1
    FIRST_QUARTER = 2
    WAXING_GIBBOUS = 3
    FULL_MOON = 4
    WANING_GIBBOUS = 5
    LAST_QUARTER = 6
    WANING_CRESCENT = 7


class Moon:

    def __init__(self, now: datetime = datetime.now()):
        self._position = None
        self.set_position(now)

    def set_position(self, now: datetime):
        diff = now - datetime(2001, 1, 1)
        days = Decimal(diff.days) + (Decimal(diff.seconds) / Decimal(86400))
        lunations = Decimal("0.20439731") + (days * Decimal("0.03386319269"))
        self._position = lunations % Decimal(1)

    def get_phase(self):
        index = (self._position * Decimal(8)) + Decimal("0.5")
        index = math.floor(index)
        return MoonPhase(int(index) & 7)
