from models.admin import Admin
from models.hotel_system import HotelSystem

class Main:
    def __init__(self):
        self.hotel_system = HotelSystem()
        self.run_loop()

    def run_loop(self):
        while True:
            print('1. Search Rooms')
            print('2. Create Reservation')
            print('3. Check Out')
            print('4. View Reservation')
            print('5. Modify Bookings')
            print('6. Access Admin Actions')
            print('7. List all rooms')
            print('8. Exit')

            choice = input('Enter your choice: ').strip()
            match choice:
                case '1':
                    self.search_rooms()

                case '2':
                    self.hotel_system.make_reservation()

                case '3':
                    self.hotel_system.check_out()

                case '4':
                    self.view_reservation()

                case '5':
                    self.hotel_system.modify_booking()

                case '6':
                    # admin_id = int(print('Enter admin id: '))
                    # id(admin_id)
                    self.admin_options()

                case '7':
                    self.list_rooms()
                
                case '8':
                    print('Thank you. Have a great day.\n')
                    break

                case _:
                    print('Please select available options (1-6).\n')

    def admin_options(self):
        print('-----Admin Actions-----')
        print('1. Add Room')
        print('2. Remove Room')
        print('3. Update Room')
        print('4. Exit')
        print('-----------')

        admin_choice = input('Enter admin option: ').strip()
        admin = Admin()
        if(admin_choice == '1'):
            admin.add_rooms()
        
        elif(admin_choice == '2'):
            admin.remove_room()

        elif(admin_choice == '3'):
            admin.update_room()

        else:
            print('Redirecting to main options\n')

    def list_rooms(self):
        print('-----LIST ROOMS-----')
        self.hotel_system.list_all_rooms()

    def search_rooms(self):
        try:
            print('-----SEARCH ROOM-----')
            room_type = input('Enter room type: ').strip()
            minimum_price = float(input('Enter minimum price: '))
            maximum_price = float(input('Enter maximum price: '))
            capacity = float(input('Enter occupancy capacity: '))

            # check for price range validation
            if minimum_price > maximum_price:
                print(
                    '\nMinimum price cannot exceed maximum price.\n'
                )
                return
            
            self.hotel_system.search_room(room_type, minimum_price, maximum_price, capacity)
        except ValueError:
            print('\nInvalid input type. Please enter valid number as requested.\n')
    
    def view_reservation(self):
        res_id = input('  Reservation ID: ').strip()
        res = next((r for r in self.hotel_system._all_reservations() if r.reservation_id == res_id and r.status != "Checked Out"), None)
        if not res:
            print('\n  Reservation not found.\n')
            return
        res.generate_summary()

if __name__ == '__main__':
    Main()
