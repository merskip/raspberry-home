import unittest

from raspberry_home.main import run


class SimulatorPlatformTests(unittest.TestCase):

    @staticmethod
    def test_end_to_end():
        run(is_simulator=True, is_gui=False)


if __name__ == '__main__':
    unittest.main()
