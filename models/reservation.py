from datetime import datetime
from models.room import Room

class Reservation:
    def __init__(self, reservation_id, guest_id, room: Room, check_in, check_out, services=None):
        self.reservation_id = reservation_id
        self.guest_id = guest_id
        self.room = room
        self.check_in = check_in
        self.check_out = check_out
        self.services = services or []
        self.status = "Confirmed"

    
    def _nights(self):
        ci = datetime.strptime(self.check_in, '%Y-%m-%d')
        co = datetime.strptime(self.check_out, '%Y-%m-%d')
        return max(1, (co - ci).days)
    
 
    def calculate_fee(self):        
        SERVICE_FEE = 500
        nights = self._nights()
        room_charge = self.room.calculate_fee(nights)           
        services_charge = len(self.services) * SERVICE_FEE * nights
        return room_charge + services_charge
    
    @property
    def total_charge(self):
        return self.calculate_fee()
 

    def generate_summary(self):                 
        print(f'  Reservation ID : {self.reservation_id}')
        print(f'  Guest ID       : {self.guest_id}')
        print(f'  Room           : {self.room.room_number}')
        print(f'  Check-in       : {self.check_in}')
        print(f'  Check-out      : {self.check_out}')
        print(f'  Nights         : {self._nights()}')
        print(f'  Services       : {", ".join(self.services) if self.services else "None"}')
        print(f'  Total Charge   : ${self.total_charge:.2f}')
        print(f'  Status         : {self.status}')
 
    def cancel(self):          
        self.status = 'Cancelled'
 
    def modify_dates(self, check_in, check_out):
        self.check_in = check_in
        self.check_out = check_out