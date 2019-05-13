import unittest
import argparse

from easylib.nlp.vocabs import VocabFilter, VocabLengthFilter, VocabLineSplitor, VocabSpaceLineSplitor, VocabGenerator


class VocabsTest(unittest.TestCase):

    def testVocabGenerator(self):
        input_files = [
            '/opt/algo_nfs/kdd_luozhouyang/datas/matchpyramid/vocab.txt',
        ]
        output_file = '/opt/algo_nfs/kdd_luozhouyang/tmp/vocab.test.txt'

        filters = [
            VocabLengthFilter(10),
        ]
        splitor = VocabSpaceLineSplitor()

        g = VocabGenerator(10000, splitor, filters, min_count=1)
        g.generate(input_files, output_file)

        print(g.counter.most_common(10))

        with open(output_file, mode='rt', encoding='utf8', buffering=8192) as fin:
            for i in range(10):
                print(fin.readline().strip('\n'))


if __name__ == "__main__":
    unittest.main()

