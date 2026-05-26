class Reservation:
    def _init_(self, reservation_id, user_id, room_number, check_in, check_out):
        self.reservation_id = reservation_id
        self.user_id = user_id
        self.room_number = room_number
        self.check_in = check_in
        self.check_out = check_out