class Room:
    def __init__(self, room_id, room_number, room_type, nightly_rate, status, capacity):
        self.room_id = room_id
        self.room_number = room_number
        self.room_type = room_type
        self.nightly_rate = nightly_rate
        self.status = status
        self.capacity = capacity

    def display_info(self):
        print(
            f"Room {self.room_number} |"
            f"{self.room_type} |"
            f"{self.nightly_rate} |"
            f"{self.status}"
        )

    def set_status(self, status):
        self.status = status

    def is_available(self):
        return self.status.lower() == "active"