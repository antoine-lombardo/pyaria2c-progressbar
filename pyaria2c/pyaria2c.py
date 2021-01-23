import tempfile, os, subprocess

COMPLETED_STR = '] Download complete:'

class Pyaria2c():
    def __init__(self, exec_path: str, on_progress=None, on_finish=None):
        self.exec_path = exec_path
        self.on_progress = on_progress
        self.on_finish = on_finish

    def download(self, urls, filenames, directory=None):
        if not filenames is None:
            if not len(filenames) == len(urls):
                return -1
        with tempfile.TemporaryDirectory() as tmp_dir:

            # generate urls file
            urls_filename = os.path.join(tmp_dir, 'urls.txt')
            with open(urls_filename, mode='wt') as file:
                for i in range(len(urls)):
                    file.write((urls[i] + '\n'))
                    filename = None
                    if not filenames is None:
                        file.write(('  out={}\n'.format(filenames[i])))

            # create the command
            exec_path = os.path.abspath(self.exec_path)
            command = [exec_path, '-i', urls_filename]
            if not directory is None:
                command.extend(['-d', os.path.abspath(directory)])
            else:
                command.extend(['-d', os.getcwd()])
            command.extend(['--log', '-', '--console-log-level', 'warn'])

            # start the process
            process = subprocess.Popen(command, stdout=subprocess.PIPE,
                                       universal_newlines=True, shell=False, bufsize=-1)

            # watching loop
            n_files = len(urls)
            c = 0
            while process.poll() is None:
                try:
                    line = process.stdout.readline()
                    if COMPLETED_STR in line:
                        percent = int(100 * c / n_files)
                        if not self.on_progress is None:
                            self.on_progress(percent)
                        c += 1
                except: continue

        # call the on finish hook
        if not self.on_finish is None:
            self.on_finish(process.poll())
