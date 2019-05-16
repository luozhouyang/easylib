import os
import logging

logger = logging.getLogger('easylib')


class FileMerger:

    def __init__(self,
                 read_mode='rt',
                 write_mode='wt',
                 read_encoding='utf8',
                 write_encoding='utf8',
                 read_buffering=8192,
                 write_buffering=8192):
        self.read_mode = read_mode
        self.write_mode = write_mode
        self.read_encoding = read_encoding
        self.write_encoding = write_encoding
        self.read_buffering = read_buffering
        self.write_buffering = write_buffering

    def merge_files(self, input_files, output_file):
        path, name = os.path.split(output_file)
        if not os.path.exists(path):
            os.makedirs(path)
        with open(output_file, mode=self.write_mode, encoding=self.write_encoding,
                  buffering=self.write_buffering) as fout:
            for f in input_files:
                if not os.path.exists(f):
                    logger.info('File does not exist: %s' % f)
                    continue
                with open(f, mode=self.read_mode, encoding=self.read_encoding, buffering=self.read_buffering) as fin:
                    for line in fin:
                        fout.write(line)
                logger.info('Finished write %s to %s' % (f, output_file))
        logger.info('Done!')
