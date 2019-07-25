import sys
from platform.platform import Platform
from stub.stub_platform import StubPlatform


def get_platform() -> Platform:
    is_simulator_arg = len(sys.argv) > 1 and str(sys.argv[1]) == "simulator"
    if is_simulator_arg:
        return StubPlatform()
    else:
        from platform_impl import PlatformImpl
        return PlatformImpl()


if __name__ == "__main__":
    platform = get_platform()
    print(platform)
