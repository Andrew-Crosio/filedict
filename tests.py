import os
import tempfile
import unittest

from filedict import FileDict


test_data_raw = {'test': 'data', 1: 2, 'three': 4}
test_data = "(dp0\nS'test'\np1\nS'data'\np2\nsI1\nI2\nsS'three'\np3\nI4\ns."


class ShouldReadFromFileTestCases(unittest.TestCase):
    def setUp(self):
        _, self.file_path = tempfile.mkstemp('_filedict_test_file')
        with open(self.file_path, 'w') as temp_file:
            temp_file.write(test_data)

    def tearDown(self):
        os.remove(self.file_path)

    def test_should_read_from_file_when_trying_to_get(self):
        file_dict = FileDict(self.file_path)
        self.assertEqual(file_dict.get('wrong'), None)
        self.assertDictEqual(file_dict, test_data_raw)

    def test_should_read_from_file_when_trying_to_iterate(self):
        file_dict = FileDict(self.file_path)
        keys = [key for key in file_dict]
        self.assertEqual(keys, test_data_raw.keys())

    def test_should_read_from_file_when_trying_to_get_item(self):
        file_dict = FileDict(self.file_path)
        self.assertEqual(file_dict['test'], test_data_raw['test'])


