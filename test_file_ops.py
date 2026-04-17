import os
import tempfile
import unittest

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


class TestFileOps(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.base_dir = self.temp_dir.name

    def tearDown(self):
        self.temp_dir.cleanup()

    def test_create_write_read_delete_rename(self):
        file_path = os.path.join(self.base_dir, "example.txt")
        ok, path = create_file(file_path, "hello", overwrite=False)
        self.assertTrue(ok)
        self.assertTrue(os.path.exists(path))

        content = read_file(file_path)
        self.assertEqual(content, "hello")

        ok, path = write_file(file_path, "world")
        self.assertTrue(ok)
        self.assertEqual(read_file(file_path), "world")

        ok, path = append_file(file_path, "!")
        self.assertTrue(ok)
        self.assertEqual(read_file(file_path), "world!")

        info = file_info(file_path)
        self.assertIsNotNone(info)
        self.assertEqual(info["size_bytes"], 6)

        ok, path = rename_file(file_path, "renamed.txt")
        self.assertTrue(ok)
        self.assertTrue(os.path.exists(path))
        self.assertFalse(os.path.exists(file_path))

        ok, path = delete_file(path)
        self.assertTrue(ok)
        self.assertFalse(os.path.exists(path))

    def test_list_search_change_directory(self):
        file1 = os.path.join(self.base_dir, "one.txt")
        file2 = os.path.join(self.base_dir, "two.log")
        create_file(file1, "one")
        create_file(file2, "two")

        results = list_files(self.base_dir, include_dirs=False)
        self.assertIn(file1, results)
        self.assertIn(file2, results)

        matches = search_files(self.base_dir, "one")
        self.assertEqual(matches, [file1])

        ok, path = change_directory(self.base_dir)
        self.assertTrue(ok)
        self.assertEqual(path, os.path.abspath(self.base_dir))


if __name__ == "__main__":
    unittest.main()
