import os


class FileLineReadCallback:

    def read_line(self, line):
        raise NotImplementedError()


class FileLineStripCallback(FileLineReadCallback):

    def read_line(self, line):
        if not line:
            return None
        line = line.strip('\n')
        return line


class FileLineReader:
    """Read a file line by line."""

    def __init__(self, callbacks=None, params=None):
        """Init.

        Args:
            callbacks: A list of `FileLineReadCallback` instance or a list of functions, whose signature: fun(line: str) -> Any
            params: A dict, override the default params.
        """
        default_params = self.default_params()
        if params:
            default_params.update(params)
        self.params = default_params

        self.callbacks = callbacks

    def read_file(self, filename):
        if not os.path.exists(filename):
            print('Files does not exist: %s' % filename)
            return
        with open(filename, mode=self.params['mode'], encoding=self.params['encoding'],buffering=self.params['buffering']) as fin:
            for line in fin:
                if self.callbacks:
                    for c in self.callbacks:
                        if isinstance(c, FileLineReadCallback):
                            # instance of FileLineReadCallback
                            c.read_line(line)
                        else:
                            # a function, signature is: fun(line:str) -> Any
                            c(line)

    def read_files(self, files):
        for f in files:
            self.read_file(f)

    def default_params(self):
        p = {
            'mode': 'rt',
            'encoding': 'utf8',
            'buffering': 8192,
        }
        return p
