from models.user import User
from models.room import Room
from models.hotel_system import HotelSystem
class Admin(User):
    def __init__(self):
        super().__init__()

    # add rooms
    def add_rooms(self):
        room_id = int(input('Enter room id: '))
        room_name = input('Enter room name: ')
        room_type = input('Enter room type: ')
        price = float(input('Enter room price: '))
        capacity = int(input('Enter room capacity: '))
        
        # create new room object with user input
        new_room = Room(room_id, room_name, room_type, price, 'Available', capacity)

        # create new hotel_system object to add room in a system
        new_system = HotelSystem(new_room)
        new_system.add_rooms()