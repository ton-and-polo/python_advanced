import unittest
from server import process


class TestServer(unittest.TestCase):
    def setUp(self):
        self.client_message = {
            'action': 'presence',
            'time': 'Thu Oct 17 10:31:17 2019',
            'user': {'account_name': 'guest'}
        }

        self.server_message = {'response': 200}

    def test_process(self):
        self.assertEqual(self.server_message, process(self.client_message))
        self.assertIsInstance(process(self.client_message), dict)


if __name__ == '__main__':
    unittest.main()