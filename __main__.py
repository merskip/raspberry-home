import sys

if __name__ == "__main__":
    is_simulator = "--simulator" in sys.argv
    from raspberry_home.main import run
    run(is_simulator=is_simulator)
