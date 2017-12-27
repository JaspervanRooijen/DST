from bs4 import BeautifulSoup
import os


class File:
    file_name = None
    file = None

    def open_file(self, path):
        if self.file is not None:
            self.file.close()
        try:
            # path = os.getcwd().replace("\\", "/")
            # path += '/'+file_name
            self.file = open(path, 'r+')
            self.file_name = path.split('\\')[-1]
            return True
        except IOError:
            return False

    def get_bs(self):
        return BeautifulSoup(self.file.read())

    def close_file(self):
        if self.file is not None:
            self.file.close()

    def write_file(self, cont):
        path = os.getcwd().replace("\\", "/")
        path += '/tmp/'
        if not os.path.exists(path):
            os.makedirs(path)
        path += self.file_name
        f = open(path, 'w')
        f.write(cont)
        f.close()
        return f

    def write_file_full(self, cont, file_name):
        path = os.getcwd().replace("\\", "/")
        path += '/tmp/'
        if not os.path.exists(path):
            os.makedirs(path)
        path += file_name
        f = open(path, 'w')
        f.write(cont)
        f.close()
        self.file = f
        self.file_name = file_name
        return f
