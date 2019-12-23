import unittest
from decorator import logThis
import os
import time

logfile_name = 'test_logfile.log'
sleep_time = 0.01


class TestDecorator(unittest.TestCase):
    def test_logThis(self):
        @logThis(filename=logfile_name, timed=True)
        def sleep(sleep_time):

            time.sleep(sleep_time)

        sleep(sleep_time)

        with open(logfile_name, 'rt') as file:

            self.assertEqual(len(list(file)), 1)

    @classmethod
    def tearDownClass(self):

        os.remove(logfile_name)


if __name__ == '__main__':
    unittest.main()
