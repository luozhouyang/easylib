import os


class FileSpliter:
    """Split a file to multi parts."""

    def split(self, file, num_parts, output_dir):
        """Split file.

        Args:
            file: The path of file.
            num_parts: The number of parts you want to split
            output_dir: A dir to save the split parts files
        """
        total_lines = self._count_file_lines(file)
        lines_each_part = int(total_lines // num_parts)
        if total_lines % num_parts == 0:
            self._split_file(file, num_parts, lines_each_part, output_dir)
        else:
            self._split_file(file, num_parts + 1, lines_each_part, output_dir)

    def _split_file(self, file, parts, lines_each_part, output_dir):
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
        path, name = os.path.split(file)
        with open(file, mode='rt', encoding='utf8', buffering=8192) as fin:
            for i in range(parts):
                p = os.path.join(output_dir, name + '.part' + str(i))
                with open(p, mode='wt', encoding='utf8', buffering=8192) as fout:
                    for j in range(lines_each_part):
                        line = fin.readline()
                        if not line:
                            break
                        fout.write(line)

    def _count_file_lines(self, f):
        with open(f) as f:
            for i, l in enumerate(f):
                pass
        return i + 1
