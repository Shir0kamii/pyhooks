from pyhooks import precall_register, postcall_register, Hook


class FileManager(object):

    def __init__(self, filename):
        self.filename = filename

    @Hook
    def write(self, text):
        self.file.write(text)


class TextfileManager(FileManager):

    @precall_register('write')
    def open_file(self, *args):
        self.file = open(self.filename, 'w')

    @postcall_register('write')
    def close_file(self, *args):
        self.file.close()


TextfileManager("testing.txt").write("This is a test.")
