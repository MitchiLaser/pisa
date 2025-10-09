#!/usr/bin/env python3

import logging as log
import json
import sys


class cluster_conf:

    class node_conf:
        def __init__(self, device: str | dict, global_task_limit: int):
            # parse address first
            if isinstance(device, str):
                self.address = device
            elif isinstance(device, dict):
                if 'device' not in device:
                    log.error(f"Missing 'device' field in configuration for device {device}")
                    sys.exit(1)
                self.address = device['device']
            else:
                log.error("Invalid device entry in cluster configuration")
                sys.exit(1)
            # task limit is an optional parameter, if not present revert back to global task limit
            self.task_limit = global_task_limit if not ('num_tasks' in device) else device['num_tasks']
            log.debug(f"Node {self.address} with task limit {self.task_limit} initialized")

        def get_address(self) -> str:
            return self.address

        def get_task_limit(self) -> int:
            return self.task_limit

    def __init__(self, config):
        # copy the content of the 'all' object in the configuration file
        if 'all' not in config:
            log.error("Missing 'all' object in cluster configuration")
            sys.exit(1)
        self.global_param = config['all']
        if ('num_tasks' not in self.global_param) or (not isinstance(self.global_param['num_tasks'], int)) or (self.global_param['num_tasks'] < 1):
            log.error("Missing or invalid global task limit in cluster configuration")
            sys.exit(1)

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
