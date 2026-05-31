import pandas as pd
import os
from utils.file_operations import FileOperations
from datetime import datetime
from models.guest import Guest
from models.room import Room
from models.reservation import Reservation
from enums.room_status import RoomStatus

SERVICES = ["Breakfast", "Airpot transfer", "Parking Slot", "Laundry Service", "Spa Access"]


class HotelSystem:
    def __init__(self, room = None):
        self.room = room
        self.room_file_path = 'data/rooms.xlsx'
        self.booking_file_path = 'data/bookings.xlsx'
        self.guests = [] # reservations live on guest now 
        self._preload_data()

        # create data folder if it doesn't exist, to save rooms data
        os.makedirs('data', exist_ok=True)
        

    def _preload_data(self):
        # load bookings from file and rebuild guests list
        if not os.path.exists(self.booking_file_path):
            return
        df = pd.read_excel(self.booking_file_path)
        if df.empty:
            return
        for _, row in df.iterrows():
            guest_id   = str(row['Guest ID'])
            guest_name = str(row['Guest Name'])
            room_obj   = Room(None, str(row['Room Number']), str(row['Room Type']),
                              float(row['Nightly Rate']), str(row['Room Status']), int(row['Capacity']))
            svcs = str(row['Services']).split('|') if str(row['Services']) != 'nan' else []
            res  = Reservation(str(row['Reservation ID']), guest_id, room_obj,
                               str(row['Check In']), str(row['Check Out']), svcs)
            res.status       = str(row['Status'])

            # find existing guest or create one
            guest = self._find_guest_by_id(guest_id)
            if not guest:
                guest = Guest(guest_id, guest_name, '')
                self.guests.append(guest)
            guest.make_booking(res)
    
    # add room
    def add_rooms(self):
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
        if os.path.exists(self.room_file_path):
            existing_data = pd.read_excel(self.room_file_path)
            # check for same room id already exists
            if self.room.room_id in existing_data['Room ID'].values:
                print("Room ID already exists.")
                return
            updated_data = pd.concat([existing_data, new_row], ignore_index=True)  # append
            updated_data.to_excel(self.room_file_path, index=False)
        else: # else, create a new file
            new_row.to_excel(self.room_file_path, index=False)

        print(f'Room {self.room.room_id} saved successfully.')


    # list rooms available
    def list_all_rooms(self):
       room_list = FileOperations.read_file(self.room_file_path)
       if len(room_list) > 0:
        print('Available Rooms:\n', room_list)

    # search room based on user input
    def search_room(self, room_type, minimum_price, maximum_price, capacity):
        results = FileOperations.search_file(self.room_file_path)
        # check if file exists before search to prevent project crashing
        if results.empty:
            print('No room available in the system. \n')
            return None
        print(RoomStatus.AVAILABLE.value)

        # Search for Room ID, Capacity, Room Number and only Available rooms
        formatted_results = results[
            (results['Status'] == RoomStatus.AVAILABLE.value) &
            (results['Room Type'].astype(str).str.contains(room_type, case=False)) &
            (results['Capacity'] == capacity) &
            (results['Price'] >= minimum_price) & (results['Price'] <= maximum_price)
        ]

        if formatted_results.empty:
            print('\nSorry! No matching rooms found for your request".\n')
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
                if res.status in  ("Checked Out", "Cancelled"):
                    continue
                ex_in = datetime.strptime(res.check_in, fmt)
                ex_out = datetime.strptime(res.check_out, fmt)
                
                if new_in < ex_out and new_out > ex_in:
                    return False # overlap found
        
        return True
    
    def _all_reservations(self):
        return [r for guest in self.guests for r in guest.bookings]
    
    def _find_guest_by_id(self, guest_id):
        return next((g for g in self.guests if g.guest_id == guest_id), None)
    

    def _save_bookings(self):                                   
        all_res = self._all_reservations()
        if not all_res:
            return
        guest_map = {r.reservation_id: g for g in self.guests for r in g.bookings}
        data = [{
            'Reservation ID': r.reservation_id,
            'Guest ID'      : r.guest_id,
            'Guest Name'    : guest_map[r.reservation_id].name,
            'Room Number'   : r.room.room_number,
            'Room Type'     : r.room.room_type,
            'Nightly Rate'  : r.room.nightly_rate,
            'Room Status'   : r.room.status,
            'Capacity'      : r.room.capacity,
            'Check In'      : r.check_in,
            'Check Out'     : r.check_out,
            'Services'      : '|'.join(r.services),
            'Total Charge'  : r.total_charge,
            'Status'        : r.status,
        } for r in all_res]
        pd.DataFrame(data).to_excel(self.booking_file_path, index=False)


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
        self._save_bookings()

    
    def modify_booking(self):
        print('\n Modify Booking')
        res_id = input('  Reservation ID: ').strip()
        res = next((r for r in self._all_reservations() if r.reservation_id == res_id and r.status != "Checked Out"), None)
        
        if not res:
            print('\n  Reservation not found.\n')
            return
 
        res.generate_summary()
        print('\n  What to modify?')
        print('  1. Check-in date')
        print('  2. Change room')
        choice = input('  Choice: ').strip()
 
        if choice == '1':
            new_date = input("New check-in date (YYYY-MM-DD): ").strip()
            res.check_in = new_date
            print('\n  Check-in time updated.')
 
        elif choice == '2':
            rooms = FileOperations.read_file(self.room_file_path)
            available = rooms[rooms['Status'].str.lower() == 'available']
            
            if available.empty:
                print('\n  No other rooms available.\n')
                return
            
            print('\n  Available rooms:')
            print(available[['Room Number', 'Room Type', 'Price', 'Capacity']].to_string(index=False))
            new_room = input('\n  New room number: ').strip()
            match = rooms[rooms['Room Number'].astype(str).str.lower() == new_room.lower()]
            
            if match.empty or match.iloc[0]['Status'].lower() != 'available':
                print('\n  Room not available.\n')
                return
            
            if not self.validate_no_overlap(new_room, res.check_in.split()[0], res.check_out):
                print('\n  New room already booked for those dates.\n')
                return
            
            rooms.loc[rooms['Room Number'].astype(str).str.lower() == res.room.room_number.lower(), 'Status'] = 'Available'
            rooms.loc[rooms['Room Number'].astype(str).str.lower() == new_room.lower(), 'Status'] = 'Occupied'
            rooms.to_excel(self.room_file_path, index=False)
            
            new_room_obj = Room(None, new_room, match.iloc[0]['Room Type'], float(match.iloc[0]['Price']), 'Occupied', int(match.iloc[0]['Capacity']))
            
            res.room = new_room_obj
            res.total_charge = res.calculate_fee()
            print('\n  Room updated.')
 
        else:
            print('\n  Invalid choice.\n')
            return
 
        print('\n  Updated reservation:')
        res.generate_summary()
        self._save_bookings()


    def check_out(self):
        print('\nCheck-out')
        res_id = input('  Reservation ID: ').strip()
        res = next((r for r in self._all_reservations() if r.reservation_id == res_id and r.status == 'Confirmed'), None)
        
        if not res:
            print('\n  Reservation not found or already checked out.\n')
            return
 
        res.status = 'Checked Out'
 
        rooms = FileOperations.read_file(self.room_file_path)
        rooms.loc[rooms['Room Number'].astype(str).str.lower() == res.room.room_number.lower(), 'Status'] = 'Available'
        rooms.to_excel(self.room_file_path, index=False)
 
        print('\n  Final bill:')
        res.generate_summary()
        self._save_bookings
        print('\n  Thank you for your stay!\n')