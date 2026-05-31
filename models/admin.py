from models.user import User
from models.room import Room
from models.hotel_system import HotelSystem
from utils.file_operations import FileOperations
from enums.room_status import RoomStatus
class Admin(User):
    def __init__(self):
        super().__init__()
        self.room_file_path = 'data/rooms.xlsx'

    # add rooms
    def add_rooms(self):
        room_id = int(input('Enter room id: '))
        room_name = input('Enter room name: ')
        room_type = input('Enter room type: ')
        price = float(input('Enter room price: '))
        capacity = int(input('Enter room capacity: '))
        # create new room object with user input
        new_room = Room(room_id, room_name, room_type, price, RoomStatus.AVAILABLE.value, capacity)

        # create new hotel_system object to add room in a system
        new_system = HotelSystem(new_room)
        new_system.add_rooms()

    
    # update room status
    def update_room_status(self):
        room_id = int(input('Enter room id: '))
        print('Choose new status to update')
        print('1. Available')
        print('2. Maintenance')
        print('3. Inactive')

        status = int(input('Enter the available options: '))
        print('Status', status)
        results = FileOperations.search_file(self.room_file_path)
        # check if room with room_id exists
        if room_id not in results['Room ID'].values:
            print("Room not found.")
            return
        
         # update room status based on the user input
        results.loc[results['Room ID'] == room_id,
            'Status'] = (RoomStatus.AVAILABLE.value if status == 1 else 
                         RoomStatus.MAINTENANCE.value if status == 2 else 
                         RoomStatus.INACTIVE.value)

        # now save the updated row in excel file
        results.to_excel(
            self.room_file_path,
            index=False
        )

        print(
            f"Room {room_id} status updated."
        )