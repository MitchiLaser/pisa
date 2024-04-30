#!/usr/bin/env python3

from .metadata import __version__
import argparse
import json
import logging as log
import sys


def main():
    """
    The main function is a necessary entry point for the application. This makes it possible to call it like an executable.
    To enable this feature the pyproject.toml file needs to contain a function which can be called by the python interpreter.
    """

    # set up argument parser
    parser = argparse.ArgumentParser(
        prog="PISA",
        description="Python SSH Infrastructure for Scalable Applications (PISA)"
    )
    parser.add_argument("-v", "--version", action="version", version=f"%(prog)s {__version__}")
    parser.add_argument("-c", "--cluster", required=True, help="cluster configuration file")
    parser.add_argument("-t", "--task", required=True, help="task configuration file")
    parser.add_argument("-d", "--debug", action="store_true", help="enable debug mode which prints the application logs to the console")
    args = parser.parse_args()

    # set up log
    log.basicConfig(level=log.DEBUG if args.debug else log.WARNING)
    log.debug(f"Cluster configuration file: {args.cluster}")
    log.debug(f"Task configuration file: {args.task}")

    # open and read cluster configuration file
    try:
        with open(args.cluster, "r", encoding=sys.getfilesystemencoding()) as f:
            cluster = json.load(f)
            # check if user accidentally has no device in the list
            if len(cluster['devices']) == 0:
                log.error("No devices listed in cluster configuration file")
                sys.exit(1)
            # some debugging print statements
            log.debug(f"Global task limit: {cluster['all']['num_tasks']} task(s) on every machine")
            log.debug(f"List of available devices: {', '.join(cluster['devices'])}")
            # TODO: continue after config file was parsed
    except Exception as e:
        log.error(f"Failed to read cluster configuration file: {args.cluster}")
        log.error(e)
        sys.exit(1)


if __name__ == "__main__":
    main()
