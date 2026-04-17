import os


def clear_screen():
    command = "cls" if os.name == "nt" else "clear"
    os.system(command)


def pause(message="Press Enter to continue..."):
    try:
        input(f"{message}")
    except KeyboardInterrupt:
        print()


def normalize_path(path, base_directory=None):
    if not path:
        return None

    path = os.path.expanduser(path)
    if os.path.isabs(path):
        return os.path.abspath(path)

    if base_directory:
        return os.path.abspath(os.path.join(base_directory, path))

    return os.path.abspath(path)
