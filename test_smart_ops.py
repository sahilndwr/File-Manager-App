import os
import tempfile
import unittest

from smart_ops import (
    detect_duplicate_files,
    disk_usage_analysis,
    optimized_search,
    organize_files_by_type,
)


class TestSmartOps(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.base_dir = self.temp_dir.name

    def tearDown(self):
        self.temp_dir.cleanup()

    def create_file(self, name, content):
        path = os.path.join(self.base_dir, name)
        with open(path, "w", encoding="utf-8") as handle:
            handle.write(content)
        return path

    def test_organize_files_by_type(self):
        txt_path = self.create_file("readme.txt", "hello")
        img_path = self.create_file("photo.jpg", "binary")
        other_path = self.create_file("script.py", "print(1)")

        moved = organize_files_by_type(self.base_dir)
        self.assertEqual(len(moved), 3)

        self.assertTrue(os.path.exists(os.path.join(self.base_dir, "Documents", "readme.txt")))
        self.assertTrue(os.path.exists(os.path.join(self.base_dir, "Images", "photo.jpg")))
        self.assertTrue(os.path.exists(os.path.join(self.base_dir, "Other", "script.py")))

    def test_detect_duplicate_files(self):
        self.create_file("a.txt", "same")
        self.create_file("b.txt", "same")
        self.create_file("A.txt", "different")

        duplicates = detect_duplicate_files(self.base_dir)
        self.assertTrue(any(len(group) > 1 for group in duplicates["content"]))
        self.assertTrue(any(len(group) > 1 for group in duplicates["name"]))

    def test_disk_usage_analysis(self):
        self.create_file("small.txt", "1")
        self.create_file("large.txt", "x" * 1024)

        report = disk_usage_analysis(self.base_dir)
        self.assertEqual(report["file_count"], 2)
        self.assertTrue(report["total_size"] >= 1025)
        self.assertEqual(report["largest_files"][0][1], os.path.join(self.base_dir, "large.txt"))

    def test_optimized_search(self):
        self.create_file("find_me.txt", "hello")
        self.create_file("ignore.me", "hello")

        matches = optimized_search(self.base_dir, name_query="find_me", extension=".txt")
        self.assertEqual(len(matches), 1)
        self.assertTrue(matches[0][0].endswith("find_me.txt"))


if __name__ == "__main__":
    unittest.main()
