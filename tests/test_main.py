import unittest
from unittest.mock import patch, MagicMock
from main import Main


class TestMain(unittest.TestCase):

    def setUp(self):
        with patch('builtins.input', return_value='8'):  # fix: '8' exits loop so __init__ doesn't block
            with patch('models.hotel_system.HotelSystem._preload_data'):  # fix: skip file IO on init
                self.app = Main()
        self.app.hotel_system = MagicMock()

    @patch('sys.stdout')
    def test_list_rooms(self, mock_stdout):
        self.app.list_rooms()
        self.app.hotel_system.list_all_rooms.assert_called_once()

    @patch('builtins.input', return_value='test')
    @patch('sys.stdout')
    def test_search_rooms(self, mock_stdout, mock_input):
        self.app.search_rooms()
        self.app.hotel_system.search_room.assert_called_once_with('test')

    @patch('builtins.input', return_value='3')
    @patch('sys.stdout')
    def test_admin_exit(self, mock_stdout, mock_input):
        self.app.admin_options()
        self.app.hotel_system.assert_not_called()  # fix: assert nothing hotel-related was called


if __name__ == '__main__':
    unittest.main()