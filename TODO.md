# TODO

## Update Pool of running processes

When the ssh connection to an existing device fails, the thread that was assigned to handle this connection terminates itself. Therefore, when in the beginning more devices are available than threads are spawned, all unnecessary threads stop themself first. In case, the remaining threads all have a problem with the SSH connection, there is no thread left to handle the remaining tasks and the program freezes.
