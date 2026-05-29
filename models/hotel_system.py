import pandas as pd
import os
from utils.file_operations import FileOperations
from datetime import datetime
from models.guest import Guest
from models.room import Room
from models.reservation import Reservation

SERVICES = ["Breakfast", "Airpot transfer", "Parking Slot", "Laundry Service", "Spa Access"]


class HotelSystem:
    def __init__(self, room = None):
        self.room = room
        self.room_file_path = 'data/rooms.xlsx'
        self.guests = [] # reservations live on guest now 

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
       if len(room_list) > 0:
        print('Available Rooms:\n', room_list)

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

        print('Searched results:\n', formatted_results)

    
    def validate_no_overlap(self, room_number, check_in, check_out):
        fmt = "%Y-%m-%d"
        new_in = datetime.strptime(check_in,fmt)
        new_out = datetime.strptime(check_out, fmt)

        for guest in self.guests:
            for res in guest.bookings:
                if res.room.room_number.lower() != room_number.lower():
                    continue
                if res.status == "Checked Out": # if they checked out, this needs work
                    continue
                ex_in = datetime.strptime(res.check_in, fmt)
                ex_out = datetime.strptime(res.check_out, fmt)
                
                if new_in < ex_out and new_out > ex_in:
                    return False # overlap found
        
        return True
    
    def _all_reservations(self):
        return [r for guest in self.guests for r in guest.bookings]
    
    def _find_guest_by_id(self, guest_id):
        return next((g for g in self.guests if g.guest == guest_id), None)
    

    def make_reservation(self):
        print("\nMake a reservation\n")
        guest_id = input("Guest Id: ").strip()
        name = input("Name: ").strip()

        guest = self._find_guest_by_id(guest_id)
        if not guest:
            guest = Guest(guest_id, name, "")
            self.guests.append(guest)
        
        rooms = FileOperations.read_file(self.room_file_path)
        available = rooms[rooms['Status'].str.lower() == 'available']
        
        if available.empty:
            print('\n  No rooms available.\n')
            return
        
        print('\n  Available rooms:')
        print(available[['Room Number', 'Room Type', 'Price', 'Capacity']].to_string(index=False))
 
        room_number = input('\n  Room number: ').strip()
        
        match = rooms[rooms['Room Number'].astype(str).str.lower() == room_number.lower()]
        if match.empty or match.iloc[0]['Status'].lower() != 'available':
            print('\n  Room not available.\n')
            return
        
        nightly_rate = float(match.iloc[0]['Price'])
        capacity = int(match.iloc[0]['Capacity'])
        room_obj = Room(None, room_number, match.iloc[0]['Room Type'], nightly_rate, 'Occupied', capacity)
 
        check_in_date = input('  Check-in date  (YYYY-MM-DD) : ').strip()
        check_out     = input('  Check-out date (YYYY-MM-DD) : ').strip()
 
        if not self.validate_no_overlap(room_number, check_in_date, check_out):
            print('\n  Room already booked for those dates.\n')
            return
        

        # optional services, services are not defined yet, just keeping it here as placeholder for later
        print('\n  Optional services ($500/service/night):')
        for i, s in enumerate(SERVICES, 1):
            print(f'    {i}. {s}')
        print('    0. Skip')
        picks = input('  Select (e.g. 1 3) or 0: ').strip().split()
        services = []
        for p in picks:
            if p == '0': break
            try:
                idx = int(p) - 1
                if 0 <= idx < len(SERVICES):
                    services.append(SERVICES[idx])
            except ValueError:
                pass

        res_id = f'R{1000 + len(self._all_reservations()) + 1}'
        reservation = Reservation(res_id, guest_id, room_obj, check_in_date, check_out, services)
        guest.make_booking(reservation)
 
        rooms.loc[rooms['Room Number'].astype(str).str.lower() == room_number.lower(), 'Status'] = 'Occupied'
        rooms.to_excel(self.room_file_path, index=False)
 
        print('\n  Reservation confirmed!')
        reservation.generate_summary()