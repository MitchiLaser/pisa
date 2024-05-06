#!/usr/bin/env python3

from .config import __version__
from .dispatcher import dispatcher
import argparse
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
        description="Pseudo Infrastructure for Scalable Applications (PISA)"
    )
    parser.add_argument("-v", "--version", action="version", version=f"%(prog)s {__version__}")
    parser.add_argument("-c", "--cluster", required=True, help="cluster configuration file")
    parser.add_argument("-t", "--task", required=True, help="task configuration file")
    parser.add_argument("-l", "--log", action="store_true", help="enable debug log printing to the console")
    parser.add_argument("-d", "--dry-run", action="store_true", help="do not run anything, only show which tasks would be run and create assignment file (useful for recreation of assignment file)")
    args = parser.parse_args()

    # set up log
    log.basicConfig(
        level=log.DEBUG if args.log else log.WARNING,
        # format="%(acsctime)s - %(levelname)s - %(message)s",
        format='%(asctime)s %(levelname)-8s %(message)s',
        datefmt="%Y-%m-%d %H:%M:%S"
    )
    log.debug(f"Cluster configuration file: {args.cluster}")
    log.debug(f"Task configuration file: {args.task}")

    # open and read cluster configuration file
    cluster = dispatcher.cluster_conf.parse_file(args.cluster)
    tasks = dispatcher.task_list.parse_file(args.task)

    # in case of a dry run: print all tasks and exit
    if args.dry_run:
        while (not tasks.empty()):
            task = tasks.get()
            print(task)
        sys.exit(0)

    # start the cluster dispatcher
    dispatcher.run_dispatcher(
        cluster=cluster,
        tasks=tasks
    )


if __name__ == "__main__":
    main()
