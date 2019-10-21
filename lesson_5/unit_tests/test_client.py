import unittest
from client import presence_message, process


class TestClient(unittest.TestCase):
    def setUp(self):
        self.client_message = presence_message()
        self.required_keys = ['action', 'time', 'user']
        self.test_message = {
            'action': 'presence',
            'time': 'Thu Oct 17 10:31:17 2019',
            'user': {'account_name': 'guest'}
        }

        self.server_message = {'response': 200}

    def test_presence(self):
        self.client_message['time'] = self.test_message['time']
        self.assertEqual(self.test_message, self.client_message)
        self.assertTrue([key in presence_message().keys() for key in self.required_keys])

    def test_process(self):
        self.assertEqual(200, process(self.server_message))
        self.assertNotEqual(400, process(self.server_message))


if __name__ == '__main__':
    unittest.main()
