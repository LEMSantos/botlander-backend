import unittest

import botlander


class BotlanderTestCase(unittest.TestCase):

    def setUp(self):
        self.app = botlander.app.test_client()

    def test_index(self):
        rv = self.app.get('/')
        self.assertIn('Welcome to botlander', rv.data.decode())


if __name__ == '__main__':
    unittest.main()
