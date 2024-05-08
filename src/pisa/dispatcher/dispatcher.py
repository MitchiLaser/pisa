#!/usr/bin/env python3

from . import cluster_conf
from ..ssh import ssh
from . import task_list
import threading
import logging as log
import queue
import subprocess
import sys

import random  # TODO: remove


def run_dispatcher(cluster: cluster_conf.cluster_conf, tasks: queue.Queue[task_list.task]):
    # Start a thread for each connection to every device (task_limit for each node). Then these start taking tasks from the queue.
    for node in cluster.node_list():
        for _ in range(node.get_task_limit()):
            threading.Thread(target=node_connection, args=(node, tasks)).start()

    tasks.join()  # wait for the queue to be emptied by all threads
    if not tasks.empty():
        log.error("not all tasks were executed")
        sys.exit(1)


def node_connection(node: cluster_conf.cluster_conf.node_conf, tasks: queue.Queue[task_list.task]):
    while True:
        try:
            # get a task from the queue
            task = tasks.get(block=False)
            has_task = True
            log.debug(f"Task {task.num} starting on node {node.get_address()}: {task.cmd}")

            ssh.Session(node.get_address()) \
                .connect() \
                .send_command(f"cd {task.w_dir}") \
                .send_command(f"./{task.env}/bin/activate") \
                .send_command(f"mkdir -p {task.out}") \
                .send_command(f"mkdir -p {task.err}") \
                .send_command(f"{task.cmd} >{task.out}/{task.num}.out 2>{task.err}/{task.num}.err &") \
                .close()
            # log.debug(f"{task.cmd} >{task.out}/{task.num}.out 2>{task.err}/{task.num}.err &")  # TODO: remove
        except queue.Empty:  # queue is empty: exit thread
            has_task = False
            break
        except FileNotFoundError as e:  # file not found: program is not available
            log.error(f"file not found: {e}")
            tasks.put(task)  # reinsert task back into the queue
            break
        except subprocess.CalledProcessError as e:  # return code does not equal zero
            log.error(f"error while executing command: {e}")
            if e.returncode == 255:  # return code 255 can only be returned by ssh
                log.error(f"Assuming that the node ({node.get_address()}) is not reachable. Ending thread.")
                tasks.put(task)  # reinsert task back into the queue
                break
            else:
                log.error(f"Executing command {task.num} failed: {task.cmd}")
        else:
            log.debug(f"Task {task.num} finished on node {node.get_address()}: {task.cmd}")
        finally:
            tasks.task_done() if has_task else None  # task from the queue always needs to be marked as done
