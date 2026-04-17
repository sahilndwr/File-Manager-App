import os
import time
import tkinter as tk
from tkinter import filedialog, messagebox, simpledialog, ttk

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
from utils import normalize_path


class FileManagerApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Smart File System Manager")
        self.geometry("900x640")
        self.current_dir = os.getcwd()
        self.create_widgets()

    def create_widgets(self):
        menu = tk.Menu(self)
        self.config(menu=menu)

        file_menu = tk.Menu(menu, tearoff=0)
        file_menu.add_command(label="Exit", command=self.quit)
        menu.add_cascade(label="File", menu=file_menu)

        help_menu = tk.Menu(menu, tearoff=0)
        help_menu.add_command(label="File operation guide", command=self.show_operation_guide)
        help_menu.add_command(label="About", command=self.show_about)
        menu.add_cascade(label="Help", menu=help_menu)

        header_frame = ttk.Frame(self, padding=(10, 8))
        header_frame.pack(fill=tk.X)
        ttk.Label(header_frame, text="Smart File System Manager", font=("Segoe UI", 18, "bold")).pack(side=tk.LEFT)
        self.directory_label = ttk.Label(header_frame, text=f"Current directory: {self.current_dir}")
        self.directory_label.pack(side=tk.RIGHT)

        notebook = ttk.Notebook(self)
        notebook.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)

        self.file_tab = ttk.Frame(notebook)
        self.smart_tab = ttk.Frame(notebook)
        notebook.add(self.file_tab, text="File Operations")
        notebook.add(self.smart_tab, text="Smart Operations")

        self.create_file_tab()
        self.create_smart_tab()
        self.create_output_panel()

    def create_file_tab(self):
        frame = ttk.Frame(self.file_tab, padding=10)
        frame.pack(fill=tk.BOTH, expand=True)

        row = 0
        buttons = [
            ("Create file (new file)", self.on_create_file),
            ("Read file (view content)", self.on_read_file),
            ("Write file (overwrite content)", self.on_write_file),
            ("Append file (add text to end)", self.on_append_file),
            ("Delete file (remove file)", self.on_delete_file),
            ("Rename file (change filename)", self.on_rename_file),
            ("File info (view metadata)", self.on_file_info),
            ("List directory (show files)", self.on_list_files),
            ("Search files (find by name)", self.on_search_files),
            ("Change directory (select folder)", self.on_change_directory),
        ]

        for label, command in buttons:
            button = ttk.Button(frame, text=label, command=command)
            button.grid(row=row // 2, column=row % 2, sticky=tk.EW, padx=2, pady=4)
            row += 1

        frame.columnconfigure(0, weight=1)
        frame.columnconfigure(1, weight=1)

    def create_smart_tab(self):
        frame = ttk.Frame(self.smart_tab, padding=10)
        frame.pack(fill=tk.BOTH, expand=True)

        ttk.Button(frame, text="Organize files by type", command=self.on_organize_files).grid(row=0, column=0, sticky=tk.EW, padx=2, pady=4)
        ttk.Button(frame, text="Detect duplicate files", command=self.on_detect_duplicates).grid(row=1, column=0, sticky=tk.EW, padx=2, pady=4)
        ttk.Button(frame, text="Disk usage analysis", command=self.on_disk_usage).grid(row=2, column=0, sticky=tk.EW, padx=2, pady=4)
        ttk.Button(frame, text="Optimized search", command=self.on_optimized_search).grid(row=3, column=0, sticky=tk.EW, padx=2, pady=4)

        frame.columnconfigure(0, weight=1)

    def create_output_panel(self):
        output_frame = ttk.LabelFrame(self, text="Output", padding=10)
        output_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=(0, 10))
        self.output_text = tk.Text(output_frame, height=14, wrap=tk.WORD)
        self.output_text.pack(fill=tk.BOTH, expand=True)
        self.output_text.configure(state=tk.DISABLED)

    def show_about(self):
        messagebox.showinfo("About", "Smart File System Manager\nPython frontend for file operations and optimization.")

    def show_operation_guide(self):
        guide = tk.Toplevel(self)
        guide.title("File Operation Guide")
        guide.geometry("620x520")

        text_frame = ttk.Frame(guide, padding=10)
        text_frame.pack(fill=tk.BOTH, expand=True)

        text_widget = tk.Text(text_frame, wrap=tk.WORD)
        text_widget.pack(fill=tk.BOTH, expand=True)
        text_widget.insert("1.0",
            "Core File Operations:\n\n"
            "1. Create: Makes a new file. Fails if the file exists.\n\n"
            "2. Read: Opens the file and displays content.\n\n"
            "3. Write: Overwrites the file completely with new content.\n"
            "   Existing content is deleted first.\n\n"
            "4. Append: Adds text to the end of the file without deleting existing content.\n\n"
            "5. Delete: Removes the file from the system.\n\n"
            "6. Rename: Changes the file name.\n\n"
            "7. File info: Shows file size, modified time, and metadata.\n\n"
            "8. List/Search: Shows or finds files in a folder.\n\n"
            "Write vs Append:\n"
            "- Write overwrites the file.\n"
            "- Append keeps the old content and adds new text at the end.\n\n"
            "Shortcut explanation for viva:\n"
            "\"Write overwrites the file, while append adds data without removing existing content.\"\n"
        )
        text_widget.configure(state=tk.DISABLED)

        button_frame = ttk.Frame(guide, padding=(10, 0))
        button_frame.pack(fill=tk.X)
        ttk.Button(button_frame, text="Close", command=guide.destroy).pack(side=tk.RIGHT)

    def append_output(self, message):
        self.output_text.configure(state=tk.NORMAL)
        self.output_text.insert(tk.END, f"{message}\n")
        self.output_text.see(tk.END)
        self.output_text.configure(state=tk.DISABLED)

    def show_view_window(self, path, content):
        viewer = tk.Toplevel(self)
        viewer.title(f"View: {os.path.basename(path)}")
        viewer.geometry("700x520")

        notice = ttk.Label(viewer, text="Editing this file will overwrite its content when you save.", foreground="darkred")
        notice.pack(fill=tk.X, padx=10, pady=(10, 0))

        text_frame = ttk.Frame(viewer, padding=8)
        text_frame.pack(fill=tk.BOTH, expand=True)

        text_widget = tk.Text(text_frame, wrap=tk.WORD)
        text_widget.pack(fill=tk.BOTH, expand=True)
        text_widget.insert("1.0", content)

        button_frame = ttk.Frame(viewer, padding=8)
        button_frame.pack(fill=tk.X)

        def on_save():
            data = text_widget.get("1.0", tk.END)
            ok, message = write_file(path, data)
            if ok:
                messagebox.showinfo("Save complete", f"Saved changes to {path}")
                self.append_output(f"Saved changes to {path}")
            else:
                messagebox.showerror("Save failed", message)

        ttk.Button(button_frame, text="Save changes", command=on_save).pack(side=tk.LEFT, padx=4)
        ttk.Button(button_frame, text="Close", command=viewer.destroy).pack(side=tk.RIGHT, padx=4)

    def show_file_selection_window(self, title, action_label, action_callback):
        files = list_files(self.current_dir, include_dirs=False)
        if not files:
            messagebox.showinfo(title, "No files found in the current directory.")
            return

        selector = tk.Toplevel(self)
        selector.title(title)
        selector.geometry("560x360")

        ttk.Label(selector, text=f"Current directory: {self.current_dir}").pack(anchor=tk.W, padx=10, pady=(10, 0))

        list_frame = ttk.Frame(selector, padding=8)
        list_frame.pack(fill=tk.BOTH, expand=True)

        scrollbar = ttk.Scrollbar(list_frame, orient=tk.VERTICAL)
        listbox = tk.Listbox(list_frame, yscrollcommand=scrollbar.set, selectmode=tk.SINGLE)
        scrollbar.config(command=listbox.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        for path in files:
            listbox.insert(tk.END, os.path.basename(path))

        button_frame = ttk.Frame(selector, padding=8)
        button_frame.pack(fill=tk.X)

        def on_action():
            selection = listbox.curselection()
            if not selection:
                messagebox.showwarning(title, "Please select a file first.")
                return
            selected_path = files[selection[0]]
            selector.destroy()
            action_callback(selected_path)

        ttk.Button(button_frame, text=action_label, command=on_action).pack(side=tk.RIGHT, padx=4)
        ttk.Button(button_frame, text="Cancel", command=selector.destroy).pack(side=tk.RIGHT)

    def show_file_names_window(self, title, items):
        window = tk.Toplevel(self)
        window.title(title)
        window.geometry("560x360")

        list_frame = ttk.Frame(window, padding=8)
        list_frame.pack(fill=tk.BOTH, expand=True)

        scrollbar = ttk.Scrollbar(list_frame, orient=tk.VERTICAL)
        listbox = tk.Listbox(list_frame, yscrollcommand=scrollbar.set)
        scrollbar.config(command=listbox.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        for item in items:
            listbox.insert(tk.END, os.path.basename(item) if os.path.isabs(item) else item)

        close_frame = ttk.Frame(window, padding=8)
        close_frame.pack(fill=tk.X)
        ttk.Button(close_frame, text="Close", command=window.destroy).pack(side=tk.RIGHT)

    def ask_multiline_text(self, title, prompt, initial=""):
        dialog = tk.Toplevel(self)
        dialog.title(title)
        dialog.geometry("560x320")
        dialog.transient(self)
        dialog.grab_set()

        ttk.Label(dialog, text=prompt).pack(anchor=tk.W, padx=12, pady=(12, 0))
        text_widget = tk.Text(dialog, wrap=tk.WORD, height=14)
        text_widget.pack(fill=tk.BOTH, expand=True, padx=12, pady=8)
        text_widget.insert("1.0", initial)

        button_frame = ttk.Frame(dialog)
        button_frame.pack(fill=tk.X, padx=12, pady=(0, 12))

        result = {"value": None}

        def on_ok():
            result["value"] = text_widget.get("1.0", tk.END).rstrip("\n")
            dialog.destroy()

        def on_cancel():
            dialog.destroy()

        ttk.Button(button_frame, text="OK", command=on_ok).pack(side=tk.RIGHT, padx=4)
        ttk.Button(button_frame, text="Cancel", command=on_cancel).pack(side=tk.RIGHT)

        self.wait_window(dialog)
        return result["value"]

    def ask_text(self, title, prompt, initial=""):
        return simpledialog.askstring(title, prompt, initialvalue=initial, parent=self)

    def ask_directory(self, title="Select directory"):
        return filedialog.askdirectory(title=title, initialdir=self.current_dir) or None

    def ask_file(self, title="Select file", save=False, default_extension=None):
        if save:
            return filedialog.asksaveasfilename(title=title, initialdir=self.current_dir, defaultextension=default_extension)
        return filedialog.askopenfilename(title=title, initialdir=self.current_dir)

    def on_create_file(self):
        path = self.ask_file("Create file", save=True, default_extension=".txt")
        if not path:
            return
        content = self.ask_multiline_text("Create file", "Enter initial content:") or ""
        ok, message = create_file(path, content, overwrite=False)
        if ok:
            self.append_output(f"Created: {message}")
        else:
            self.append_output(f"Create failed: {message}")

    def on_read_file(self):
        path = self.ask_file("Read file")
        if not path:
            return
        try:
            content = read_file(path)
            self.show_view_window(path, content)
        except Exception as exc:
            self.append_output(f"Read failed: {exc}")

    def on_write_file(self):
        path = self.ask_file("Write file")
        if not path:
            return
        try:
            content = read_file(path)
            self.show_view_window(path, content)
        except Exception as exc:
            self.append_output(f"Write failed: {exc}")

    def on_append_file(self):
        path = self.ask_file("Append file")
        if not path:
            return
        content = self.ask_multiline_text("Append file", "Enter content to append:") or ""
        ok, message = append_file(path, content)
        self.append_output(f"Append {'succeeded' if ok else 'failed'}: {message}")

    def on_delete_file(self):
        def delete_path(path):
            ok, message = delete_file(path)
            self.append_output(f"Delete {'succeeded' if ok else 'failed'}: {message}")

        self.show_file_selection_window("Delete file", "Delete selected file", delete_path)

    def on_rename_file(self):
        def rename_path(path):
            new_name = self.ask_text("Rename file", "Enter new file name:")
            if not new_name:
                return
            ok, message = rename_file(path, new_name)
            self.append_output(f"Rename {'succeeded' if ok else 'failed'}: {message}")

        self.show_file_selection_window("Rename file", "Rename selected file", rename_path)

    def on_file_info(self):
        def show_info(path):
            info = file_info(path)
            if info:
                result = (
                    f"Path: {info['path']}\n"
                    f"Size: {self.format_bytes(info['size_bytes'])}\n"
                    f"Created: {time.ctime(info['created'])}\n"
                    f"Modified: {time.ctime(info['modified'])}\n"
                    f"Is directory: {info['is_directory']}"
                )
                self.append_output(result)
            else:
                self.append_output("File not found.")

        self.show_file_selection_window("File info", "Show selected file info", show_info)

    def on_list_files(self):
        directory = self.ask_directory("Select directory to list")
        if not directory:
            return

        entries = list_files(directory, include_dirs=True)
        if entries:
            self.show_file_names_window(f"Files in {directory}", entries)
        else:
            self.append_output("No files found or directory not accessible.")

    def on_search_files(self):
        query = self.ask_text("Search files", "Enter search query:")
        if query is None:
            return
        extension = self.ask_text("Search files", "Enter extension filter (optional, e.g. .txt):") or None
        matches = search_files(self.current_dir, query, extension)
        if matches:
            self.append_output(f"Search results for '{query}':")
            for path in matches:
                self.append_output(f"  {path}")
        else:
            self.append_output("No matching files found.")

    def on_change_directory(self):
        directory = self.ask_directory("Change current directory")
        if not directory:
            return
        ok, message = change_directory(directory)
        if ok:
            self.current_dir = message
            self.directory_label.config(text=f"Current directory: {self.current_dir}")
            self.append_output(f"Changed directory to {self.current_dir}")
        else:
            self.append_output(f"Change directory failed: {message}")

    def on_organize_files(self):
        moved = organize_files_by_type(self.current_dir)
        if moved:
            self.append_output("Organized files:")
            for src, dest in moved:
                self.append_output(f"  {src} -> {dest}")
        else:
            self.append_output("No files were moved.")

    def on_detect_duplicates(self):
        duplicates = detect_duplicate_files(self.current_dir)
        if duplicates["content"]:
            self.append_output("Duplicates by content:")
            for group in duplicates["content"]:
                self.append_output("  Group:")
                for path in group:
                    self.append_output(f"    {path}")
        else:
            self.append_output("No duplicate content found.")

        if duplicates["name"]:
            self.append_output("Duplicates by name:")
            for group in duplicates["name"]:
                self.append_output("  Group:")
                for path in group:
                    self.append_output(f"    {path}")
        else:
            self.append_output("No duplicate names found.")

    def on_disk_usage(self):
        report = disk_usage_analysis(self.current_dir)
        self.append_output(f"Disk usage for {self.current_dir}:")
        self.append_output(f"  Total files: {report['file_count']}")
        self.append_output(f"  Total size: {self.format_bytes(report['total_size'])}")
        self.append_output("  Largest files:")
        for size, path in report["largest_files"]:
            self.append_output(f"    {self.format_bytes(size)}  {path}")

    def on_optimized_search(self):
        query = self.ask_text("Optimized search", "Enter name query (optional):") or None
        extension = self.ask_text("Optimized search", "Enter extension filter (optional, e.g. .txt):") or None
        min_size = self.ask_text("Optimized search", "Minimum size in bytes (optional):")
        max_size = self.ask_text("Optimized search", "Maximum size in bytes (optional):")
        min_size = int(min_size) if min_size and min_size.isdigit() else None
        max_size = int(max_size) if max_size and max_size.isdigit() else None
        matches = optimized_search(self.current_dir, query, extension, min_size, max_size)
        if matches:
            self.append_output("Optimized search results:")
            for path, size in matches:
                self.append_output(f"  {self.format_bytes(size)}  {path}")
        else:
            self.append_output("No files matched the optimized search.")

    @staticmethod
    def format_bytes(value):
        for unit in ["B", "KB", "MB", "GB", "TB"]:
            if value < 1024:
                return f"{value:.2f} {unit}"
            value /= 1024
        return f"{value:.2f} PB"


if __name__ == "__main__":
    app = FileManagerApp()
    app.mainloop()
