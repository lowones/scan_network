#!/usr/bin/python
import multiprocessing
import subprocess
import os

def pinger( job_q, results_q):
    DEVNULL = open(os.devnull, 'w')
    while True:
        ip = job_q.get()
        if ip is None: break

        try:
            subprocess.check_call(['ping', '-W20', '-c1', ip], stdout=DEVNULL)
            results_q.put(ip)
        except:
            pass

def main():
    pool_size = 255
    jobs = multiprocessing.Queue()
    results = multiprocessing.Queue()
    pool = [ multiprocessing.Process(target=pinger, args=(jobs,results)) for i in range(pool_size) ]

    print(pool)

    for p in pool:
        p.start()

    for i in range(1,255):
        jobs.put('10.0.1.{0}'.format(i))

    for p in pool:
        jobs.put(None)

    for p in pool:
        p.join()

    hosts = []
    while not results.empty():
        ip = results.get()
        hosts.append(int(ip.split('.')[3]))


    for h in sorted(hosts):
        print("10.0.1.%s" % str(h))

if __name__ == '__main__':
    main()
