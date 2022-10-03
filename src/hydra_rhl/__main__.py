import sys
from __init__ import __version__


def main() -> None:
    opts = [o for o in sys.argv[1:] if o.startswith("-")]

    # Show help message
    if "-v" in opts or "--version" in opts:
        print(f"Current version {__version__}")
        raise SystemExit()


if __name__ == "__main__":
    main()
