import sys

from raspberry_home.main import run

if __name__ == "__main__":
    is_simulator = "--simulator" in sys.argv
    run(is_simulator=is_simulator)
