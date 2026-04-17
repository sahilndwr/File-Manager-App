# Smart File System Handling and Optimization

This is a CLI-based Python file management application that demonstrates operating system concepts such as file handling, directory management, and storage optimization.

## Project Structure

- `main.py` - Entry point and CLI menu
- `file_ops.py` - Core file handling operations
- `smart_ops.py` - Optimization features and analysis
- `utils.py` - Helper utilities
- `gui.py` - Graphical user interface application
- `test_files/` - Sample files for testing

## Features

- Create, read, write, append, delete, and rename files
- Directory navigation and file listing
- Search files by name and extension
- Automatic file organization by type
- Duplicate file detection by name and content
- Disk usage analysis and large-file identification
- Optimized file lookup with filters

## How to Run

1. Open a terminal and change to the project directory:

```bash
cd "c:\Users\Sahil NDWR\Desktop\OS project\file_manager_app"
```

2. Run the CLI app:

```bash
python main.py
```

3. Run the GUI app:

```bash
python gui.py
```

## Run tests

```bash
python -m unittest discover tests
```

## Notes

- Use relative paths from the current directory for convenience.
- The app preserves files when organizing and handles duplicate destinations automatically.
