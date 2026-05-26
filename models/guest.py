from user import User

class Guest(User):
    def _init_(self, user_id, name, email, bookings):
        super()._init_(user_id, name, email)
        self.bookings = bookings