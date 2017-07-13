#!/usr/bin/python
import subprocess
import sys

def main():
    print("hello")
    for i in range(1, 255):
#        print(i)
        ip = "10.0.1." + str(i)
        test = subprocess.Popen(["ping", "-W", "20", "-c", "1", ip], stdout=subprocess.PIPE)
        rc =  test.wait()
        if rc == 0:
            print("\n%s"%ip)
        else:
            print("."),
            sys.stdout.flush()
#        output = test.communicate()[0]
#        print(output)



if __name__ == "__main__":
    main()
