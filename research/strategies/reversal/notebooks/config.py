import os


def set_project_root(levels_up=2):
    """
    Sets the working directory to the project root.

    Parameters:
    levels_up (int): Number of levels to go up in the directory structure to reach the root.
    """
    current_dir = os.getcwd()
    project_root = os.path.abspath(os.path.join(current_dir, *[".."] * levels_up))
    os.chdir(project_root)
