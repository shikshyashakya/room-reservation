from models.user import User

class Guest(User):
    def __init__(self, user_id, name, email, bookings=None):
        super().__init__(user_id, name, email)
        self.bookings = bookings if bookings is not None else []

    
    def view_bookings(self):
        if not self.bookings:
            print('  No reservations found.')
            return
        for r in self.bookings:
            r.generate_summary()
            print()


    def cancel_booking(self, booking_id):
        for r in self.bookings:
            if r.reservation_id == booking_id:
                r.status = 'Cancelled'
                return True
        return False
    

    def make_booking(self, reservation):                          
        self.bookings.append(reservation)


    def print_details(self):                                      
        print(f'  Guest ID : {self.guest_id}')
        print(f'  Name     : {self.name}')
        print(f'  Email    : {self.email}')
 