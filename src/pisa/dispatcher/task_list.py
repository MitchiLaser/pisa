#!/usr/bin/env python3

from ..config import task_necessary_keys, task_optional_keys
import logging as log
import queue
import sys
import tomllib
import typing


class task:
    def __init__(self, num: int, exe: str, args: str, w_dir: str, env: str, out: str, err: str):
        self.num = num
        self.cmd = str(exe) + str(args)
        self.w_dir = w_dir
        self.env = env
        self.out = out
        self.err = err

    def __repr__(self):  # print the tasks in case of a dry run
        return f"Task {self.num}: {self.cmd}; WDIR={self.w_dir}; ENV={self.env}; OUT={self.out}; ERR={self.err}"


class enumerator:
    def __init__(self) -> None:
        self.value = 0

    def next(self) -> int:
        old_value = self.value
        self.value += 1
        return old_value


# global enumerator object which is needed by the recursive fill_queue function
enum = enumerator()


class running_var:
    def __init__(self, var_argument: dict):
        # check if the necessary keys are present
        if 'arg' not in var_argument:
            log.error("Missing 'arg' field in variable argument")
            sys.exit(1)
        self.arg_name = var_argument['arg']
        # check type and perform the corresponding parsing
        match var_argument['type']:  # TODO: Implement more types
            case 'numeric':
                if not all(k in var_argument for k in ('start', 'end', 'step')):
                    log.error(f"Missing keys in numeric variable argument {self.arg_name}")
                    sys.exit(1)
                self.values = list(range(var_argument['start'], var_argument['end'] + var_argument['step'], var_argument['step']))  # inclusive upper bound
            case _:
                log.error(f"Cannot parse argument of type: {var_argument['type']}")
                sys.exit(1)

    def __repr__(self):  # only for debugging purposes but currently nowhere in use
        return f"{self.arg_name} = {self.values}"


def fill_queue(task_queue: queue.Queue, config: dict, add_args: list[running_var], current_args: str, assignto: typing.TextIO):
    # abort recursion because all vars have been added
    if len(add_args) == 0:
        num = enum.next()
        task_queue.put(task(
            num=num,
            exe=config['executable'],
            args=current_args,  # the shlex.split() function transforms a string containing a collection of arguments into a list of single arguments
            w_dir=config['woking_directory'],
            env=config['environment'],
            out=f"{config['output']}/stdout",
            err=f"{config['output']}/stderr",
        ))
        # write the task with its parameters and the corresponding number into the assignment file
        assignto.write(f"{num}, {config['executable']} {current_args}\n")
        return
    else:
        # add all values of the fist var in the list and then call the function recursively for all remaining lists
        for i in add_args[0].values:
            fill_queue(task_queue, config, add_args[1:], f"{current_args} {add_args[0].arg_name} {i}", assignto)


def parse_file(config_file: str) -> queue.Queue[task]:
    try:
        with open(config_file, "rb") as f:
            config = tomllib.load(f)
    except Exception as e:
        log.error(f"Failed to read task file: {config_file}")
        log.error(e)
        sys.exit(1)

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
    # open assignment file
    try:
        with open(config['assign'], "w+") as assignto:
            # now fill a queue with all tasks which have to be executed
            fill_queue(
                tasks := queue.Queue(),
                config,
                [
                    # walk through the list of running variables
                    running_var(i) for i in config['var_arguments']
                ],
                config['fix_arguments'],  # fixed arguments
                assignto
            )
    except Exception as e:
        log.error(f"Failed to write assignment file: {config['assign']}")
        log.error(e)
        sys.exit(1)

    log.info(f"Added {tasks.qsize()} tasks to the queue")
    # queue should contain all the tasks with fixed arguments and all the possible combinations of the variable arguments
    return tasks
