__version__ = "0.1.3"

# a list of all the keys which have to be present in the task configuration file
task_necessary_keys = {
    "woking_directory",
    "environment",
    "output",
    "assign",
    "executable",
    "var_arguments"
}

task_optional_keys = {
    "fix_arguments"
}
