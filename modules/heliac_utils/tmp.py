from subprocess import *
a=Popen(["simple", "-s", "80000","-c","1"])

for i in ["n\n", "y\n", "a.txt", "n\n"]:
    a.stdin.write(i)

