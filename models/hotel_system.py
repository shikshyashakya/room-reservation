import pandas as pd
import os
from utils.file_operations import FileOperations

class HotelSystem:
    def __init__(self, room = None):
        self.room = room
        self.room_file_path = 'data/rooms.xlsx'
        self.customers = []
        self.reservations = []

    # TODO: preload data here


    # create data folder if it doesn't exist, to save rooms data
    os.makedirs('data', exist_ok=True)
    
    # add room
    def add_rooms(self):
        # TODO: check for same room id already exists
        formatted_room = {
            'Room ID': [self.room.room_id],
            'Room Number': [self.room.room_number],
            'Room Type': [self.room.room_type],
            'Price': [self.room.nightly_rate],
            'Status': [self.room.status],
            'Capacity': [self.room.capacity]
        }
        new_row = pd.DataFrame(formatted_room)

        # check if file already exists, if yes append
        if os.path.exists('data/rooms.xlsx'):
            existing_data = pd.read_excel('data/rooms.xlsx')
            updated_data = pd.concat([existing_data, new_row], ignore_index=True)  # append
            updated_data.to_excel('data/rooms.xlsx', index=False)
        else: # else, create a new file
            new_row.to_excel('data/rooms.xlsx', index=False)

        print(f'Room {self.room.room_id} saved successfully.')
        print()

    # list rooms available
    def list_all_rooms(self):
       room_list = FileOperations.read_file(self.room_file_path)
       print('Available Rooms\n', room_list)

    # search room based on user input
    def search_room(self, user_input):
        results = FileOperations.search_file(self.room_file_path)
        # Search for Room ID, Room Type and Room Number
        formatted_results = results[
            results['Room ID'].astype(str).str.contains(user_input, case=False) |
            results['Room Type'].astype(str).str.contains(user_input, case=False) |
            results['Room Number'].astype(str).str.contains(user_input, case=False)
        ]

        if formatted_results.empty:
            print(f'\nSorry! No rooms found for "{user_input}".\n')
            return None

        print('RESULTS\n', formatted_results)