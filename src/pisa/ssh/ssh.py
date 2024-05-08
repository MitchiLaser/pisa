#!/usr/bin/env python3

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
            shell=False,
            encoding="utf-8"
        )
        return self  # monadic return

    def send_command(self, command):
        if self.ssh_process is None:
            raise Exception("SSH connection not established. Call connect() first.")
        self.ssh_process.stdin.write(command + "\n")
        self.ssh_process.stdin.flush()
        return self  # monadic return

    def wait(self):
        if self.ssh_process is None:
            raise Exception("SSH connection not established. Call connect() first.")
        self.ssh_process.wait()
        return self  # monadic return

    def close(self):
        if self.ssh_process is not None:
            self.ssh_process.stdin.write("exit\n")
            try:
                self.ssh_process.stdin.flush()
            except BrokenPipeError:
                pass
            # self.send_command("exit")
            self.wait()

    def __del__(self):
        self.close()
