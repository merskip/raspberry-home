import unittest

from raspberry_home.main import run_simulator


class SimulatorPlatformTests(unittest.TestCase):

    @staticmethod
    def test_end_to_end():
        run_simulator()


if __name__ == '__main__':
    unittest.main()
