import unittest

from .file_reader import FileLineReader, FileLineStripCallback, FileLineReadCallback


class FileLinePrintCallback(FileLineReadCallback):

    def read_line(self, line):
        print(line)


class FileReaderTest(unittest.TestCase):

    def testFileLineReader(self):
        def split_fn(line):
            return line.split(' ')

        callbacks = [
            FileLineStripCallback(),
            split_fn,
            FileLinePrintCallback(),
        ]
        r = FileLineReader(callbacks=callbacks)

        r.read_file('easylib/io/file_reader.py')


if __name__ == '__main__':
    unittest.main()
