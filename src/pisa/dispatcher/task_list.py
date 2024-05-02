#!/usr/bin/env python3

from ..config import task_necessary_keys, task_optional_keys
import logging as log
import queue
import sys
import tomllib


class task:
    def __init__(self, exe: str, args: str, w_dir: str, env: str, out: str, err: str, log: str):
        self.exe = exe
        self.args = args
        self.w_dir = w_dir
        self.env = env
        self.out = out
        self.err = err
        self.log = log

    def __repr__(self):  # print the tasks in case of a dry run
        return f"Task: {self.exe} {self.args}; WDIR={self.w_dir}; ENV={self.env}; OUT={self.out}; ERR={self.err}; LOG={self.log}"


class running_var:
    def __init__(self, arg_name: str, start: int, end: int, step: int):
        self.arg_name = arg_name
        self.values = list(range(start, end, step))

    def __repr__(self):  # only for debugging purposes but currently nowhere in use
        return f"{self.arg_name} = {self.values}"


def fill_queue(task_queue: queue.Queue, config: dict, add_args: list[running_var], current_args: str = ""):
    # abort recursion because all vars have been added
    if len(add_args) == 0:
        task_queue.put(task(
            exe=config['executable'],
            args=current_args,
            w_dir=config['woking_directory'],
            env=config['environment'],
            out=config['output'],
            err=config['error'],
            log=config['log']
        ))
        return
    else:
        # add all values of the fist var in the lost and then call the function recursively for all remaining lists
        for i in add_args[0].values:
            fill_queue(task_queue, config, add_args[1:], f"{current_args} {add_args[0].arg_name} {i}")


def parse_file(config_file: str) -> task:
    try:
        with open(config_file, "rb") as f:
            config = tomllib.load(f)

            # check if all important keys are present
            if not task_necessary_keys.issubset(config.keys()):
                log.error(f"Missing keys in task description file: {', '.join(task_necessary_keys - config.keys())}")
                sys.exit(1)
            # check if the list of variable arguments is present and not empty
            if ('var_arguments' not in config) or (len(config['var_arguments']) == 0):
                log.error("No variable arguments provided")
                sys.exit(1)
            # warn the user about unrecognized keys
            if (config.keys() - task_necessary_keys - task_optional_keys != set()):
                log.warning(f"Unknown keys in task description file: {', '.join(config.keys() - task_necessary_keys - task_optional_keys)}")

            # now fill a queue with all tasks which have to be executed
            fill_queue(
                tasks := queue.Queue(),
                config,
                [
                    running_var(i['arg'], i['start'], i['end'], i['step']) for i in config['var_arguments']
                ],  # the list of running variables
                config['fix_arguments']  # start with fixed arguments
            )

            log.info(f"Added {tasks.qsize()} tasks to the queue")
            # queue should contain all the tasks with fixed arguments and all the possible combinations of the variable arguments
            return tasks
    except Exception as e:
        log.error(f"Failed to read task file: {config_file}")
        log.error(e)
        sys.exit(1)
