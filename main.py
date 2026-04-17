import os
import time

from file_ops import (
    append_file,
    change_directory,
    create_file,
    delete_file,
    file_info,
    list_files,
    read_file,
    rename_file,
    search_files,
    write_file,
)
from smart_ops import (
    detect_duplicate_files,
    disk_usage_analysis,
    optimized_search,
    organize_files_by_type,
)
from utils import clear_screen, normalize_path, pause


def print_header(current_dir):
    print("Smart File System Handling and Optimization")
    print("=" * 40)
    print(f"Current directory: {current_dir}")
    print("=" * 40)


def print_menu():
    print("1. Create file")
    print("2. Read file")
    print("3. Write file")
    print("4. Append file")
    print("5. Delete file")
    print("6. Rename file")
    print("7. File info")
    print("8. List files")
    print("9. Search files")
    print("10. Change directory")
    print("11. Organize files by type")
    print("12. Detect duplicate files")
    print("13. Disk usage analysis")
    print("14. Optimized search")
    print("0. Exit")


def format_bytes(value):
    for unit in ["B", "KB", "MB", "GB", "TB"]:
        if value < 1024:
            return f"{value:.2f} {unit}"
        value /= 1024
    return f"{value:.2f} PB"


def prompt_path(default_dir, description="Enter file path"):
    raw = input(f"{description} (relative to current directory works): ").strip()
    return normalize_path(raw, base_directory=default_dir)


def prompt_directory(default_dir):
    raw = input("Enter directory path: ").strip()
    return normalize_path(raw, base_directory=default_dir)


def main():
    current_dir = os.getcwd()

    while True:
        clear_screen()
        print_header(current_dir)
        print_menu()
        choice = input("Choose an option: ").strip()

        if choice == "0":
            print("Goodbye!")
            break

        if choice == "1":
            target = prompt_path(current_dir, "Create file")
            content = input("Enter initial content (leave blank for empty file): \n")
            overwrite = False
            if os.path.exists(target):
                answer = input("File exists. Overwrite? (y/N): ").strip().lower()
                overwrite = answer == "y"
            ok, message = create_file(target, content, overwrite=overwrite)
            print("File created:", message if ok else message)

        elif choice == "2":
            target = prompt_path(current_dir, "Read file")
            try:
                content = read_file(target)
                print("\n--- File content ---")
                print(content)
                print("--- End of file ---\n")
            except Exception as error:
                print("Error:", error)

        elif choice == "3":
            target = prompt_path(current_dir, "Write file")
            content = input("Enter content to write: \n")
            ok, message = write_file(target, content)
            print("Write result:", message if ok else message)

        elif choice == "4":
            target = prompt_path(current_dir, "Append file")
            content = input("Enter content to append: \n")
            ok, message = append_file(target, content)
            print("Appended to:", message if ok else message)

        elif choice == "5":
            target = prompt_path(current_dir, "Delete file")
            ok, message = delete_file(target)
            print("Delete result:", message if ok else message)

        elif choice == "6":
            target = prompt_path(current_dir, "Rename file")
            new_name = input("Enter new file name: ").strip()
            ok, message = rename_file(target, new_name)
            print("Rename result:", message if ok else message)

        elif choice == "7":
            target = prompt_path(current_dir, "File info")
            info = file_info(target)
            if info:
                print(f"Path: {info['path']}")
                print(f"Size: {format_bytes(info['size_bytes'])}")
                print(f"Created: {time.ctime(info['created'])}")
                print(f"Modified: {time.ctime(info['modified'])}")
                print(f"Directory: {info['is_directory']}")
            else:
                print("File not found.")

        elif choice == "8":
            directory = prompt_directory(current_dir)
            entries = list_files(directory, include_dirs=True)
            if entries:
                print("Files and directories:")
                for path in entries:
                    print(path)
            else:
                print("No files found or directory does not exist.")

        elif choice == "9":
            query = input("Enter search query: ").strip()
            extension = input("Filter by extension (optional, e.g. .txt): ").strip() or None
            matches = search_files(current_dir, query, extension)
            if matches:
                print("Search results:")
                for path in matches:
                    print(path)
            else:
                print("No matching files found.")

        elif choice == "10":
            target = prompt_directory(current_dir)
            ok, message = change_directory(target)
            if ok:
                current_dir = message
                os.chdir(current_dir)
                print("Changed directory to", current_dir)
            else:
                print("Error:", message)

        elif choice == "11":
            moved = organize_files_by_type(current_dir)
            if moved:
                print("Organized files:")
                for src, dest in moved:
                    print(f"{src} -> {dest}")
            else:
                print("No files were moved.")

        elif choice == "12":
            duplicates = detect_duplicate_files(current_dir)
            print("Duplicates by content:")
            if duplicates["content"]:
                for group in duplicates["content"]:
                    print("- Group:")
                    for path in group:
                        print(f"  {path}")
            else:
                print("No duplicate content found.")

            print("\nDuplicates by name:")
            if duplicates["name"]:
                for group in duplicates["name"]:
                    print("- Group:")
                    for path in group:
                        print(f"  {path}")
            else:
                print("No duplicate names found.")

        elif choice == "13":
            report = disk_usage_analysis(current_dir)
            print(f"Total files: {report['file_count']}")
            print(f"Total disk usage: {format_bytes(report['total_size'])}")
            print("Largest files:")
            for size, path in report["largest_files"]:
                print(f"{format_bytes(size)}  {path}")

        elif choice == "14":
            query = input("Enter name query (optional): ").strip() or None
            extension = input("Filter by extension (optional): ").strip() or None
            min_size = input("Minimum size in bytes (optional): ").strip()
            max_size = input("Maximum size in bytes (optional): ").strip()
            min_size = int(min_size) if min_size.isdigit() else None
            max_size = int(max_size) if max_size.isdigit() else None
            matches = optimized_search(current_dir, query, extension, min_size, max_size)
            if matches:
                print("Optimized search results:")
                for path, size in matches:
                    print(f"{format_bytes(size)}  {path}")
            else:
                print("No files matched the optimized search.")

        else:
            print("Invalid option. Please choose again.")

        pause()


if __name__ == "__main__":
    main()
