#!/usr/bin/env python3

import logging as log
import json
import sys


class cluster_conf:

    class node_conf:
        def __init__(self, address: str, task_limit: int):
            self.address = address
            self.task_limit = task_limit

        def get_address(self) -> str:
            return self.address

        def get_task_limit(self) -> int:
            return self.task_limit

    def __init__(self, config):
        # copy the content of the 'all' object in the configuration file
        if 'all' not in config:
            log.error("Missing 'all' object in cluster configuration")
            sys.exit(1)
        self.global_param = config['all']  # TODO: Check if the 'num_tasks' is also set -> list of necessary arguments in the config file

        # copy the list of nodes
        if ('devices' not in config) or (len(config['devices']) == 0):
            log.error("No devices listed in cluster configuration")
            sys.exit(1)
        self.nodes = [self.node_conf(i, self.global_param['num_tasks']) for i in config['devices']]  # TODO: check if a node has multiple entries in the config file. When yes -> overwrite and

    def node_list(self) -> list[node_conf]:
        return self.nodes

    def globals(self) -> dict:
        return self.global_param


def parse_file(config_file: str) -> cluster_conf:
    try:
        with open(config_file, "r", encoding=sys.getfilesystemencoding()) as f:
            cluster = cluster_conf(json.load(f))
            # some debugging print statements
            log.debug(f"Global task limit: {cluster.globals()['num_tasks']} task(s) on every machine")
            log.debug(f"List of available devices: {', '.join([i.address for i in cluster.node_list()])}")
            return cluster
    except Exception as e:
        log.error(f"Failed to read cluster configuration file: {config_file}")
        log.error(e)
        sys.exit(1)
