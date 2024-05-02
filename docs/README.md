# pisa
Pseudo Infrastructure for Scalable Applications (PISA)

PISA was designed to run only on the computing pool at the physics faculty at KIT. There are currently no plans to make PISA run on any other platform.

The mentioned computing pool is a collection of 34 homogeneous systems where the user home directories are mounted via NFS. PISA has a list of all the available machines and connects to every one of them via SSH. There it starts the process from a list of tasks which are given to it. Each process runs on another machine. The output is collected and stored in a file. In the end PISA separates the output of all processes and keeps track of the processes which it tried to run.
