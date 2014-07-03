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

        self.file_dict = FileDict(self.file_path)

    def tearDown(self):
        os.remove(self.file_path)

    def test_should_read_from_file_when_trying_to_get(self):
        self.assertEqual(self.file_dict.get('wrong'), None)
        self.assertDictEqual(self.file_dict, test_data_raw)

    def test_should_read_from_file_when_trying_to_iterate(self):
        keys = [key for key in self.file_dict]
        self.assertEqual(keys, test_data_raw.keys())

    def test_should_read_from_file_when_trying_to_get_item(self):
        self.assertEqual(self.file_dict['test'], test_data_raw['test'])


class ShouldWriteToFileTestCases(unittest.TestCase):
    def setUp(self):
        _, self.file_path = tempfile.mkstemp('_filedict_test_file')
        self.file_dict = FileDict(self.file_path)

    def tearDown(self):
        os.remove(self.file_path)

    def test_should_write_to_file_when_updating(self):
        self.file_dict.update(test_data_raw)
        self.assertDictEqual(FileDict(self.file_path), self.file_dict)

    def test_should_write_to_file_when_setting_item(self):
        self.file_dict['dude'] = 1
        self.assertEqual(FileDict(self.file_path)['dude'], 1)

    def test_should_write_to_file_when_popping_key(self):
        self.file_dict.update(test_data_raw)
        self.assertEqual(self.file_dict.pop('test'), test_data_raw['test'])
        new_dict = FileDict(self.file_path)
        new_data = test_data_raw.copy()
        new_data.pop('test')
        self.assertDictEqual(new_dict, new_data)

    def test_should_write_to_file_when_deleting_key(self):
        self.file_dict.update(test_data_raw)
        del self.file_dict['test']
        new_dict = FileDict(self.file_path)
        new_data = test_data_raw.copy()
        del new_data['test']
        self.assertDictEqual(new_dict, new_data)



