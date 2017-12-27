import subprocess
import os


class Verifier:
    def verify(self, file, query):
        print(query)
        verify = subprocess.check_output(["verifyta", file.name, query], shell=True)
        str_verify = str(verify)
        print("Str_verify: %s" % str_verify)
        mean = None
        for word in str_verify.split(' '):
            if 'mean' in word:
                print(word)
                mean = word
        return mean

    def simulate(self, file, query):
        path = os.getcwd().replace('\\', '/')
        path += '/tmp'
        if not os.path.exists(path):
            os.makedirs(path)
        path += '/q2.q'
        f = open(path, 'w')
        f.write(query)
        print('File: ' + file.name)
        print('QueryFile: ' + f.name)
        f.close()
        verify = subprocess.check_output(["verifyta", file.name, f.name], shell=True)
        str_verify = str(verify)
        print(str_verify)
        return verify

