import os
from collections import Counter


class VocabLineSplitor:
    """Vocab line splitor interface."""

    def split(self, line):
        """Split line to a list of vocabs.

        Args:
            line: A python string. Maybe None.

        Returns:
            A list of vocabs.
        """
        raise NotImplementedError()


class VocabSpaceLineSplitor(VocabLineSplitor):
    """Split line by space."""

    def split(self, line):
        if not line:
            return []
        return line.split(' ')


class VocabFilter:
    """Vocab filter interface."""

    def filter(self, vocab):
        """Filter this vocab if return True, else keep it.

        Args:
            vocab: A python string, vocab

        Returns:
            True if remove this vocab, False to keep this vocab.
        """
        raise NotImplementedError()


class VocabLengthFilter(VocabFilter):
    """Filter vocab if it's length greater than max_len limit."""

    def __init__(self, max_len=10):
        self.max_len = max_len

    def filter(self, vocab):
        if not vocab:
            return True
        return len(vocab) > self.max_len


class VocabEmptyFilter(VocabFilter):
    """Filter empty string."""

    def filter(self, vocab):
        if not vocab:
            return True
        return False


class VocabSpecialTokensFilter(VocabFilter):
    """Filter special tokens."""

    def __init__(self, tokens):
        self.tokens = tokens
        
    def filter(self, vocab):
        for t in self.tokens:
            vocab = vocab.replace(t, '')
            if not vocab:
                return True
        if not vocab:
            return True
        return False


class VocabGenerator:

    def __init__(self, vocab_size, line_splitor, filters=None, min_count=5, use_unk=True, sortby='freq_desc'):
        """Init.

        Args:
            vocab_size: A python integer, vocab size. Not include `<unk>`.
            line_splitor: Split a line to a list of vocabs. Instance of `VocabLineSplitor`.
            filters: An iterable, vocab filters, each element is instance of `VocabFilter`
            min_count: A python integer, word's frequency less than this will not be collected.
            use_unk: A python boolean, add `<unk>` to vocab or not.
            sortby: A python string. choices: ['freq_desc', 'alphabet_asc']
        """
        self.vocab_size = vocab_size
        self.line_splitor = line_splitor
        self.filters = filters
        self.min_count = min_count
        self.use_unk = use_unk

        if sortby not in {'freq_desc', 'alphabet_asc'}:
            raise ValueError('Invalid sortby value: %s' % sortby)
        self.sortby = sortby

        self.counter = Counter()

    def generate(self, input_files, output_file):
        """Generate vocab file.

        Args:
            input_files: An iterable, corpus files.
            output_file: The output vocab file.
        """
        for f in input_files:
            if not os.path.exists(f):
                print('File does not exist: %s' % f)
                continue
            with open(f, mode='rt', encoding='utf8', buffering=8192) as fin:
                for line in fin:
                    words = self.line_splitor.split(line.strip('\n'))
                    if not words:
                        continue
                    self.counter.update(words)
            print('Finished to count file: %s' % f)

        self._write_to_file(output_file)

    def generate_from_iterable(self, lines, output_file):
        for line in lines:
            words = self.line_splitor.split(line.strip('\n'))
            if not words:
                continue
            self.counter.update(words)
        self._write_to_file(output_file)
    
    def _write_to_file(self, output_file):
         with open(output_file, mode='wt', encoding='utf8', buffering=8192) as fout:
            vocabs = []
            for k, v in self.counter.most_common(self.vocab_size):
                if v < self.min_count:
                    continue
                if v == '<unk>':
                    continue
                if self.filters and any(vf.filter(k) for vf in self.filters):
                    continue
                vocabs.append(k)

            if self.sortby == 'alphabet_asc':
                vocabs = sorted(vocabs)
            fout.write('<unk>' + '\n')
            for v in vocabs:
                fout.write(v + '\n')


