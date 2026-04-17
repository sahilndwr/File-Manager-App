import os


def create_file(file_path, content="", overwrite=False):
    file_path = os.path.abspath(file_path)
    folder = os.path.dirname(file_path)
    os.makedirs(folder, exist_ok=True)

    if os.path.exists(file_path) and not overwrite:
        return False, "File already exists"

    with open(file_path, "w", encoding="utf-8") as handle:
        handle.write(content)

    return True, file_path


def write_file(file_path, content):
    return create_file(file_path, content, overwrite=True)


def append_file(file_path, content):
    file_path = os.path.abspath(file_path)
    folder = os.path.dirname(file_path)
    os.makedirs(folder, exist_ok=True)

    with open(file_path, "a", encoding="utf-8") as handle:
        handle.write(content)

    return True, file_path


def read_file(file_path):
    file_path = os.path.abspath(file_path)
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"File not found: {file_path}")

    with open(file_path, "r", encoding="utf-8") as handle:
        return handle.read()


def delete_file(file_path):
    file_path = os.path.abspath(file_path)
    if not os.path.exists(file_path):
        return False, "File does not exist"

    os.remove(file_path)
    return True, file_path


def rename_file(old_path, new_name):
    old_path = os.path.abspath(old_path)
    if not os.path.exists(old_path):
        return False, "Original file does not exist"

    folder = os.path.dirname(old_path)
    new_path = os.path.abspath(os.path.join(folder, new_name))
    if os.path.exists(new_path):
        return False, "Destination file already exists"

    os.rename(old_path, new_path)
    return True, new_path


def file_info(file_path):
    file_path = os.path.abspath(file_path)
    if not os.path.exists(file_path):
        return None

    stats = os.stat(file_path)
    return {
        "path": file_path,
        "size_bytes": stats.st_size,
        "created": stats.st_ctime,
        "modified": stats.st_mtime,
        "is_directory": os.path.isdir(file_path),
    }


def list_files(directory, include_dirs=False):
    directory = os.path.abspath(directory)
    if not os.path.isdir(directory):
        return []

    entries = []
    for name in sorted(os.listdir(directory)):
        full_path = os.path.join(directory, name)
        if os.path.isdir(full_path) and not include_dirs:
            continue
        entries.append(full_path)
    return entries


def search_files(directory, query, extension=None):
    directory = os.path.abspath(directory)
    matches = []

    for root, _, files in os.walk(directory):
        for name in files:
            if query.lower() in name.lower():
                if extension and not name.lower().endswith(extension.lower()):
                    continue
                matches.append(os.path.join(root, name))

    return sorted(matches)


def change_directory(path):
    path = os.path.abspath(path)
    if not os.path.isdir(path):
        return False, "Directory does not exist"

    return True, path
