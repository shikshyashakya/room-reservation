import pytest
import sys
sys.path.insert(0, '.')
from models.room import Room

def make_room(**kwargs):
    defaults = dict(room_id=1, room_number='King', room_type='Casual',
                    nightly_rate=1200.0, status='Available', capacity=2)
    defaults.update(kwargs)
    return Room(**defaults)

def test_is_available_true():
    assert make_room(status='Available').is_available() is True

def test_is_available_false():
    assert make_room(status='Occupied').is_available() is False

def test_is_available_case_insensitive():
    assert make_room(status='available').is_available() is True

def test_set_status():
    room = make_room(status='Available')
    room.set_status('Maintenance')
    assert room.status == 'Maintenance'

def test_calculate_fee_single_night():
    assert make_room(nightly_rate=1200).calculate_fee(1) == 1200.0

def test_calculate_fee_multiple_nights():
    assert make_room(nightly_rate=1200).calculate_fee(3) == 3600.0