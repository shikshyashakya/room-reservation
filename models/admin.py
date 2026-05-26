from user import User

class Admin(User):
    def _init_(self, user_id, name, email, bookings):
        super()._init_(user_id, name, email)