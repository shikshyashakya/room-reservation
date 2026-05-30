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
        print('3. Exit')
        print('-----------')

        admin_choice = input('Enter admin option: ').strip()
        if(admin_choice == '1'):
            admin = Admin()
            admin.add_rooms()
        
        elif(admin_choice == '2'):
            pass

        else:
            print('Redirecting to main options\n')

    def list_rooms(self):
        print('-----LIST ROOMS-----')
        self.hotel_system.list_all_rooms()

    def search_rooms(self):
        print('-----SEARCH ROOM-----')
        print('You can search either by Room Id, Type or Name')
        search_input = input('Enter your search: ').strip()

        if not search_input:
            print('Not acceptable! Please enter a valid search term.')
            return
        
        self.hotel_system.search_room(search_input)

    
    def view_reservation(self):
        res_id = input('  Reservation ID: ').strip()
        res = next((r for r in self.hotel_system._all_reservations() if r.reservation_id == res_id and r.status != "Checked Out"), None)
        if not res:
            print('\n  Reservation not found.\n')
            return
        res.generate_summary()

if __name__ == '__main__':
    Main()
