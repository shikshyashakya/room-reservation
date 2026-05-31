import pytest
import sys
sys.path.insert(0, '.')
from models.guest import Guest
from models.room import Room
from models.reservation import Reservation

def make_guest(**kwargs):
    defaults = dict(user_id='G1', name='Maria', email='maria@email.com')
    defaults.update(kwargs)
    return Guest(**defaults)

def make_reservation(res_id='R1001'):
    room = Room(1, 'King', 'Casual', 1200.0, 'Occupied', 2)
    return Reservation(res_id, 'G1', room, '2026-06-01', '2026-06-03')

def test_bookings_default_empty():
    assert make_guest().bookings == []

def test_bookings_parameter():
    res = make_reservation()
    guest = Guest('G1', 'Maria', 'maria@email.com', bookings=[res])
    assert len(guest.bookings) == 1

def test_make_booking():
    guest = make_guest()
    res = make_reservation()
    guest.make_booking(res)
    assert res in guest.bookings

def test_cancel_booking_success():
    guest = make_guest()
    res = make_reservation('R1001')
    guest.make_booking(res)
    result = guest.cancel_booking('R1001')
    assert result is True
    assert res.status == 'Cancelled'

def test_cancel_booking_not_found():
    guest = make_guest()
    assert guest.cancel_booking('R9999') is False

def test_multiple_bookings_independent():
    # each guest instance should have its own list
    g1 = make_guest(user_id='G1')
    g2 = make_guest(user_id='G2')
    g1.make_booking(make_reservation('R1001'))
    assert len(g2.bookings) == 0