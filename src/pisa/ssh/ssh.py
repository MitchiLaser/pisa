#!/usr/bin/env python3

import os
import subprocess


class Session:
    def __init__(self, host):
        self.host = host
        self.ssh_process = None

    def connect(self):
        self.ssh_process = subprocess.Popen(
            ["ssh", self.host],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )

        # set stdout and stderr to non blocking read mode
        os.set_blocking(self.ssh_process.stdout.fileno(), False)
        os.set_blocking(self.ssh_process.stderr.fileno(), False)

        return self  # monadic return

    def _check_connected(self):
        if self.ssh_process is None:
            raise Exception("SSH connection not established. Call connect() first.")

    def send_command(self, command):
        self._check_connected()
        try:
            self.ssh_process.stdin.write(f"{command}\n".encode('utf-8'))
            self.ssh_process.stdin.flush()
        except BrokenPipeError:
            pass
        return self  # monadic return

    def send_command_list(self, cmd_list: list):
        self._check_connected()
        for command in cmd_list:
            self.send_command(command)
            # self.ssh_process.stdin.write(f"{command}\n".encode('utf-8'))
            # self.ssh_process.stdin.flush()
        return self  # monadic return

    def read_stdout(self):
        self._check_connected()
        read = self.ssh_process.stdout.read()
        if read is not None:
            return read.decode('utf-8')

    def read_stderr(self):
        self._check_connected()
        read = self.ssh_process.stderr.read()
        if read is not None:
            return read.decode('utf-8')

    def wait_for_exit(self):
        self._check_connected()
        self.ssh_process.wait()
        returncode = self.ssh_process.returncode
        if returncode != 0:
            raise subprocess.CalledProcessError(
                returncode=returncode,
                cmd=["ssh", self.host],
                output=self.read_stdout(),
                stderr=self.read_stderr(),
            )
        return self

    def close(self):
        if self.ssh_process is not None:
            self.ssh_process.stdin.write("exit\n".encode('utf-8'))
            try:
                self.ssh_process.stdin.flush()
            except BrokenPipeError:
                pass
            self.wait_for_exit()

    def __del__(self):
        # Since 2025 Python calls __del__ outside the try ... except ... block
        # Therefore when __del__ throws an exception, it won't get caught.
        # Therefore, __del__ cannot throw an error!
        try:
            self.close()
        except Exception:
            pass
