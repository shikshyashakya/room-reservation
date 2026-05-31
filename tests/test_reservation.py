import pytest
import sys
sys.path.insert(0, '.')
from models.room import Room
from models.reservation import Reservation

def make_reservation(**kwargs):
    room = Room(1, 'King', 'Casual', 1200.0, 'Occupied', 2)
    defaults = dict(reservation_id='R1001', guest_id='G1', room=room,
                    check_in='2026-06-01', check_out='2026-06-03', services=[])
    defaults.update(kwargs)
    return Reservation(**defaults)

def test_nights_calculation():
    res = make_reservation(check_in='2026-06-01', check_out='2026-06-03')
    assert res._nights() == 2

def test_nights_minimum_one():
    res = make_reservation(check_in='2026-06-01', check_out='2026-06-01')
    assert res._nights() == 1

def test_calculate_fee_no_services():
    res = make_reservation(check_in='2026-06-01', check_out='2026-06-03', services=[])
    assert res.total_charge == 2400.0  # 1200 * 2 nights

def test_calculate_fee_with_services():
    res = make_reservation(check_in='2026-06-01', check_out='2026-06-03', services=['Breakfast', 'Parking Slot'])
    assert res.total_charge == 2400.0 + (2 * 500 * 2)  # room + 2 services * 2 nights

def test_total_charge_is_property():
    # changing room rate should reflect immediately without re-assigning
    res = make_reservation(check_in='2026-06-01', check_out='2026-06-02', services=[])
    assert res.total_charge == 1200.0
    res.room.nightly_rate = 2000.0
    assert res.total_charge == 2000.0

def test_cancel():
    res = make_reservation()
    res.cancel()
    assert res.status == 'Cancelled'

def test_modify_dates():
    res = make_reservation(check_in='2026-06-01', check_out='2026-06-03')
    res.modify_dates('2026-06-05', '2026-06-10')
    assert res.check_in == '2026-06-05'
    assert res.check_out == '2026-06-10'
    assert res._nights() == 5

def test_default_status_is_confirmed():
    assert make_reservation().status == 'Confirmed'