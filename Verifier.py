import subprocess


class Verifier:
    def verify(self, file, query):
        verify = subprocess.check_output(["verifyta", file.name, query], shell=True)
        # print("verify: %s" % verify)
        str_verify = str(verify)
        mean = None
        for word in str_verify.split(' '):
            if 'mean' in word:
                mean = word
        return mean
