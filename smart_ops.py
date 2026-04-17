import hashlib
import os
import shutil

FILE_TYPE_MAP = {
    ".txt": "Documents",
    ".md": "Documents",
    ".pdf": "Documents",
    ".doc": "Documents",
    ".docx": "Documents",
    ".xls": "Documents",
    ".xlsx": "Documents",
    ".ppt": "Documents",
    ".jpg": "Images",
    ".jpeg": "Images",
    ".png": "Images",
    ".gif": "Images",
    ".bmp": "Images",
    ".mp4": "Videos",
    ".mov": "Videos",
    ".avi": "Videos",
    ".mkv": "Videos",
    ".mp3": "Audio",
    ".wav": "Audio",
    ".zip": "Archives",
    ".rar": "Archives",
    ".7z": "Archives",
}


def _hash_file(file_path, chunk_size=4096):
    hasher = hashlib.sha256()
    with open(file_path, "rb") as handle:
        while chunk := handle.read(chunk_size):
            hasher.update(chunk)
    return hasher.hexdigest()


def organize_files_by_type(directory):
    directory = os.path.abspath(directory)
    moved = []

    for name in sorted(os.listdir(directory)):
        source_path = os.path.join(directory, name)
        if not os.path.isfile(source_path):
            continue

        _, ext = os.path.splitext(name)
        category = FILE_TYPE_MAP.get(ext.lower(), "Other")
        destination_folder = os.path.join(directory, category)
        os.makedirs(destination_folder, exist_ok=True)

        destination_path = os.path.join(destination_folder, name)
        if os.path.exists(destination_path):
            base, extension = os.path.splitext(name)
            suffix = 1
            while os.path.exists(destination_path):
                destination_path = os.path.join(destination_folder, f"{base}_{suffix}{extension}")
                suffix += 1

        shutil.move(source_path, destination_path)
        moved.append((source_path, destination_path))

    return moved


def detect_duplicate_files(directory):
    directory = os.path.abspath(directory)
    hash_map = {}
    name_map = {}

    for root, _, files in os.walk(directory):
        for name in files:
            file_path = os.path.join(root, name)
            file_hash = _hash_file(file_path)
            hash_map.setdefault(file_hash, []).append(file_path)
            name_map.setdefault(name.lower(), []).append(file_path)

    duplicates_by_content = [group for group in hash_map.values() if len(group) > 1]
    duplicates_by_name = [group for group in name_map.values() if len(group) > 1]
    return {
        "content": duplicates_by_content,
        "name": duplicates_by_name,
    }


def disk_usage_analysis(directory, top_n=10):
    directory = os.path.abspath(directory)
    files = []

    for root, _, filenames in os.walk(directory):
        for name in filenames:
            path = os.path.join(root, name)
            try:
                size = os.path.getsize(path)
            except OSError:
                size = 0
            files.append((size, path))

    files.sort(reverse=True, key=lambda entry: entry[0])
    total_size = sum(size for size, _ in files)
    return {
        "total_size": total_size,
        "file_count": len(files),
        "largest_files": files[:top_n],
    }


def optimized_search(directory, name_query=None, extension=None, min_size=None, max_size=None):
    directory = os.path.abspath(directory)
    matches = []

    for root, _, files in os.walk(directory):
        for name in files:
            if name_query and name_query.lower() not in name.lower():
                continue
            if extension and not name.lower().endswith(extension.lower()):
                continue

            path = os.path.join(root, name)
            try:
                size = os.path.getsize(path)
            except OSError:
                continue

            if min_size is not None and size < min_size:
                continue
            if max_size is not None and size > max_size:
                continue

            matches.append((path, size))

    return sorted(matches, key=lambda entry: entry[0].lower())
