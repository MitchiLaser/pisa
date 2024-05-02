# pisa
Pseudo Infrastructure for Scalable Applications (PISA)

PISA is a simple but powerful program that allows to combine the computational power of multiple computers and turn them into a batch system using only the SSH access. It is designed to be simple and therefore only runs on a some machines from the computer pool of the physics department at KIT. It is not designed to be a general purpose batch system and is only maintained for this environment. Furthermore it is not designed to be used by many users at the same time because there is no limit provided for the allocated resources (our estimation is that only one person at the time will be using it). The large benefit of PISA is that it runs completely within the userspace and requires neither root access or higher privileges for installation nor to run the program.

PISA connects to all the available machines using SSH. This only works when the authentication via an SSH key was set up before. Otherwise the connection cannot be established. Furthermore it requires the working directory (usually the home directory of all the users) to be the same on all machines. This is usual for our environment because the user home directories are mounted via NFS. The user interface is kept as simple as possible: Everything is dome from the command line. PISA gets a list of all the available machines and starts to connect to every one of them.

TODO: Write more about the architecture.
