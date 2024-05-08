#!/usr/bin/env python3

import fcntl
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

        # weird hack to transform stdout and stderr into other fds where reading is non blocking
        # first get the file descriptors of the pipes
        # then use the fcntl system call to change the file descriptor flags
        stdout_fd = self.ssh_process.stdout.fileno()
        stderr_fd = self.ssh_process.stderr.fileno()
        fcntl.fcntl(stdout_fd, fcntl.F_SETFL, os.O_NONBLOCK)
        fcntl.fcntl(stderr_fd, fcntl.F_SETFL, os.O_NONBLOCK)

        return self  # monadic return

    def _check_connected(self):
        if self.ssh_process is None:
            raise Exception("SSH connection not established. Call connect() first.")

    def send_command(self, command):
        self._check_connected()
        self.ssh_process.stdin.write(f"{command}\n".encode('utf-8'))
        self.ssh_process.stdin.flush()
        return self  # monadic return

    def read_stdout(self):
        self._check_connected()
        try:
            return self.ssh_process.stdout.read1().decode('utf-8')
        except BlockingIOError:
            return None

    def read_stderr(self):
        self._check_connected()
        try:
            return self.ssh_process.stderr.read1().decode('utf-8')
        except BlockingIOError:
            return None

    def wait(self):
        self._check_connected()
        self.ssh_process.wait()
        return self  # monadic return

    def close(self):
        if self.ssh_process is not None:
            self.ssh_process.stdin.write("exit\n".encode('utf-8'))
            try:
                self.ssh_process.stdin.flush()
            except BrokenPipeError:
                pass
            self.wait()

    def __del__(self):
        self.close()
