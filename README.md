# pisa

Pseudo Infrastructure for Scalable Applications (PISA)

PISA is a Batch-System for Python programs that uses only SSH access to the remote machines and executes Python programs. It was developed for the computer pool of the physics department at KIT but can also be used in other environments. PISA expects the computer system to be homogeneous, meaning that the user home directories are mounted via NFS and the same on all machines. Furthermore it is not designed to be used by many users at the same time because there is no limit provided for the allocated resources (our estimation is that only one person at the time will be using it). The large benefit of PISA is that it runs completely within the userspace and requires neither root access or higher privileges for installation nor to run the program.

## Installation

```bash
pip install pisa-ssh
```

## Usage

Take a look into the [Documentation-Website](https://mitchilaser.github.io/pisa/) for more information.

Short summary: PISA has a cluster configuration file (JSON, containing a list of all SSH addresses) and a task configuration file (toml). An example for both can be seen in the [config](./config) directory. This directory also contains the example program for the provided task configuration. It is a good benchmark because all the tasks take a different time to run. To run the program you have to create a virtual environment first that is sourced on the remote machines. Before you can submit jobs, the SSH keys have to be set up for passwordless login.

## Development

PISA was intentionally developed for the computing pool at the physics faculty at KIT but can be extended to other environments. I am happy to receive feedback (or issues) and contributions (pull-requests).
