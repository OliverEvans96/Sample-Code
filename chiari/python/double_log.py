#double_log.py
#import to any file
#Then call Logger('log.txt','w')
#Then all print() calls write to stdout and log.txt
#from: http://stackoverflow.com/a/616672/4228052

import sys

class Logger(object):
    def __init__(self, name, mode):
        print("Opening file for logging: {}".format(name))
        self.file = open(name, mode)
        self.stdout = sys.stdout
        sys.stdout = self
        self.lines=[]

    def write(self, data):
        #Rewrite file without last line on return carriage
        if(data=='\r'):
            self.file.write('\n')
            self.stdout.write('\r')

        #Otherwise, just write line
        else:
            self.lines.append(data)
            self.file.write(data)
            self.stdout.write(data)
            self.file.flush()

    def flush(self):
        self.file.flush()

    def __del__(self):
        sys.stdout = self.stdout
        self.file.close()
