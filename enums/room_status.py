from enum import Enum

class RoomStatus(Enum):
    AVAILABLE = 'Available'
    BOOKED = 'Booked'
    MAINTENANCE = 'Maintenance'
    INACTIVE = 'Inactive'