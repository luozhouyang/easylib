import unittest

from easylib.io import FileMerger


class FileMergerTest(unittest.TestCase):

    def testFileMerger(self):
        m = FileMerger()
        input_files = ['easylib/io/file_reader.py', 'easylib/io/file_spliter.py']
        output_file = 'testdata/merged.txt'
        m.merge_files(input_files, output_file)


if __name__ == '__main__':
    unittest.main()
