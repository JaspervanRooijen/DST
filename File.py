from bs4 import BeautifulSoup


class File:
    file_name = None
    file = None

    def open_file(self, file_name):
        if self.file is not None:
            self.file.close()
        try:
            self.file = open(file_name, 'r+')
            self.file_name = file_name
            return True
        except IOError:
            return False

    def get_bs(self):
        return BeautifulSoup(self.file.read())

    def close_file(self, file):
        if file is not None:
            self.file.close()
