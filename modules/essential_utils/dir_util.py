import os
import shutil
class dirutil():

    def __init__(self, dirpath="/opt_libfreetype.6.dylib_broken/local/share/doc/grace/examples", cmd=["xmgrace", "-noask", "-free"]):
        self.dirpath = dirpath
        self.set_dirlst()
        self.cmd = cmd    
    def set_dirlst(self, dirpath="/opt_libfreetype.6.dylib_broken/local/share/doc/grace/examples"):
        self.dirlst = os.listdir(self.dirpath)
        
    def show_dirlst(self):
        print "        File name"
        print "------------------------"
        print " %-12s%-12s" %("No.","File name")
        print "------------------------"
        for i, fname in enumerate(os.listdir(self.dirpath)): print " %-12s%-12s" %(i, fname)
        print "------------------------"

    def set_file(self, path):
        shutil.copy(path, self.dirpath)
        self.dirlst = os.listdir(self.dirpath)

    def cmd_file(self, fname, cmd=None):
        if cmd == None: cmd = self.cmd
        if "," or ":" in fname:
            flst = index_util(fname).ilst
        else:
            flst = [fname]
        for fname in flst:
            if type(fname) == int: fname = self.dirlst[fname]
            path = "%s/%s" %(self.dirpath, fname)
            Popen(cmd+[path])

def ifnonemkdir(path):
    i = os.walk(path)
    try:
        i.next()
    except:
        os.mkdir(path)

def home():
    return os.environ["HOME"]
