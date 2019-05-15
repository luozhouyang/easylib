import unittest

from easylib.io.file_spliter import FileSpliter


class FileSpliterTest(unittest.TestCase):

    def testFileSpliter(self):
        s = FileSpliter()
        input_file = 'easylib/io/file_reader.py'
        output_dir = 'testdata'
        s.split(input_file, 2, output_dir)


if __name__ == '__main__':
    unittest.main()
