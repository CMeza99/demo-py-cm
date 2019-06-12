""" __main__ to load package cm as module """
import logging
import sys

from . import cli


def main():
    """
    Main entry point.
    """
    module_args = sys.argv[1:]
    logging.debug("Module arguments received: %s", module_args)
    cli.main()


if __name__ == "__main__":
    main()
