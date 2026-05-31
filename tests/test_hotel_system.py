import pytest
import sys
import os
sys.path.insert(0, '.')
from models.hotel_system import HotelSystem
from models.room import Room
from models.guest import Guest
from models.reservation import Reservation

def make_system():
    # HotelSystem with no file IO for unit tests
    hs = HotelSystem.__new__(HotelSystem)
    hs.room = None
    hs.room_file_path = 'data/rooms.xlsx'
    hs.booking_file_path = 'data/bookings.xlsx'
    hs.guests = []
    return hs

def make_reservation(res_id, room_number, check_in, check_out, status='Confirmed'):
    room = Room(None, room_number, 'Casual', 1200.0, 'Occupied', 2)
    res = Reservation(res_id, 'G1', room, check_in, check_out)
    res.status = status
    return res

# ── validate_no_overlap ───────────────────────────────────────────

def test_no_overlap_empty_guests():
    hs = make_system()
    assert hs.validate_no_overlap('King', '2026-06-01', '2026-06-03') is True

def test_overlap_detected():
    hs = make_system()
    guest = Guest('G1', 'Maria', '')
    guest.make_booking(make_reservation('R1001', 'King', '2026-06-01', '2026-06-05'))
    hs.guests.append(guest)
    # new booking overlaps with existing
    assert hs.validate_no_overlap('King', '2026-06-03', '2026-06-07') is False

def test_no_overlap_different_room():
    hs = make_system()
    guest = Guest('G1', 'Maria', '')
    guest.make_booking(make_reservation('R1001', 'King', '2026-06-01', '2026-06-05'))
    hs.guests.append(guest)
    # same dates but different room — should be fine
    assert hs.validate_no_overlap('Queen', '2026-06-01', '2026-06-05') is True

def test_no_overlap_adjacent_dates():
    hs = make_system()
    guest = Guest('G1', 'Maria', '')
    guest.make_booking(make_reservation('R1001', 'King', '2026-06-01', '2026-06-05'))
    hs.guests.append(guest)
    # new booking starts exactly when old one ends — no overlap
    assert hs.validate_no_overlap('King', '2026-06-05', '2026-06-08') is True

def test_overlap_skips_checked_out():
    hs = make_system()
    guest = Guest('G1', 'Maria', '')
    guest.make_booking(make_reservation('R1001', 'King', '2026-06-01', '2026-06-05', status='Checked Out'))
    hs.guests.append(guest)
    # checked out reservation should not block new booking
    assert hs.validate_no_overlap('King', '2026-06-01', '2026-06-05') is True

# ── _all_reservations ─────────────────────────────────────────────

def test_all_reservations_empty():
    hs = make_system()
    assert hs._all_reservations() == []

def test_all_reservations_across_guests():
    hs = make_system()
    g1 = Guest('G1', 'Maria', '')
    g2 = Guest('G2', 'John', '')
    g1.make_booking(make_reservation('R1001', 'King', '2026-06-01', '2026-06-03'))
    g2.make_booking(make_reservation('R1002', 'Queen', '2026-06-01', '2026-06-03'))
    hs.guests = [g1, g2]
    assert len(hs._all_reservations()) == 2

# ── _find_guest_by_id ─────────────────────────────────────────────

def test_find_guest_found():
    hs = make_system()
    guest = Guest('G1', 'Maria', '')
    hs.guests.append(guest)
    assert hs._find_guest_by_id('G1') == guest

def test_find_guest_not_found():
    hs = make_system()
    assert hs._find_guest_by_id('G99') is None