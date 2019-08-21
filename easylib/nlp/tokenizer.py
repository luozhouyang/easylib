from collections import Counter
import os


class Tokenizer:

    def encode(self, vocabs):
        raise NotImplementedError()

    def decode(self, ids):
        raise NotImplementedError()


class SpaceTokenizer(Tokenizer):

    def __init__(self, corpus_files, max_vocab_size=10000, unk_id=0, unk=''):
        self.max_vocab_size = max_vocab_size
        self.unk_id = unk_id
        self.unk = unk
        self.token2id = {}
        self.id2token = {}
        self._parse_corpus(corpus_files)

    def _read_files(self, files, parse_fn):
        counter = Counter()
        for f in files:
            if not os.path.exists(f):
                print("File does not exist: %s" % str(f))
                continue
            with open(f, mode='rt', encoding='utf8', buffering=8192) as fin:
                for line in fin:
                    line = line.strip('\n')
                    if not line:
                        continue
                    words = parse_fn(line)
                    if not words:
                        continue
                    counter.update(words)
        return counter

    def _parse_corpus(self, corpus_files):
        def _parse_fn(line):
            words = line.split(' ')
            return words

        return self._read_files(corpus_files, _parse_fn)

    def encode(self, vocabs):
        return [self.token2id.get(v, self.unk_id) for v in vocabs]

    def decode(self, ids):
        return [self.id2token.get(v, self.unk) for v in ids]
