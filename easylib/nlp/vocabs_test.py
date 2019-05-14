import unittest

from easylib.nlp.vocabs import VocabGenerator, VocabLengthFilter, VocabEmptyFilter, VocabSpecialTokensFilter
from easylib.nlp.vocabs import VocabSpaceLineSplitor



class VocabsTest(unittest.TestCase):

    def testVocabGenerator(self):
        filters = [
            VocabLengthFilter(5),
            VocabEmptyFilter(),
            VocabSpecialTokensFilter(['\t', '\n']),
        ]
        splitor = VocabSpaceLineSplitor()
        g = VocabGenerator(10, splitor, filters, min_count=1)

        lines = [
            '\t \n hello world \s   \n',
        ]
        output_file = '/tmp/vocab.test.txt'

        g.generate_from_iterable(lines, output_file)


if __name__ == "__main__":
    unittest.main()
