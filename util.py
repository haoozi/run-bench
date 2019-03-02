#! /usr/bin/env python3

import os
import re
import time
import os.path
import subprocess


def run_and_get_result(param, print_param = True):
    if print_param:
        print("\033[0;32m %s \033[0m" % param)
    ret = subprocess.check_output(param)
    # return int(re.sub("[a-z]", '', strTime))
    s = ret.decode('utf-8')
    return s

def fillSSD():
    # cmd = ["sh", "Jobs/Fill.sh"]
    # ret = run_and_get_result(cmd)
    # print(ret)
    os.system("sh Jobs/Fill.sh")



def fork_and_run(param, print_param = True):
    pid = os.fork()
    if pid != 0:
        return pid

    ret = run_and_get_result(param, print_param)
    print("\033[0;32m %s \033[0m" % ret)
    exit(0)


def run_direct(cmd, print_param = True):

    print("\033[0;32m %s \033[0m" % cmd)
    os.system(cmd)


def collectBlkTrace(dev, dataDir, jobName, runTime, waitTime = 300):
    pid = os.fork()
    if pid != 0:
        return pid


    time.sleep(waitTime)
    print("\033[0;33m Launch blktrace, time: %s \033[0m" % (time.time()))


    startTime = time.time()
    targetDir = os.path.join(dataDir, "%s-blktrace-%s" % (jobName, startTime))

    ret = run_and_get_result(["blktrace", "-d", dev, "-o", targetDir, "-w", str(runTime)])
    print("\033[0;33m Blktrace complete \033[0m")
    # print(ret)
    exit(0)


# u:1023/1024,gc:0/0(0)(stop:<1024,full:>1741,free:16152/16152/16296)-0

p_rate_limiter_user = re.compile('u:[0-9]*/[0-9]*')
p_rate_limiter_gc = re.compile('gc:[0-9]*/[0-9]*')

def _getGCLog():
    """ret : [gc_enabled, gc_active, user_write, gc_write, write_amp]"""
    gc_state = ""
    write_amp = ""
    rate_limiter = ""
    ret = []

    with open("/sys/block/pblk/pblk/gc_state") as f:
        gc_state = f.read()

    with open("/sys/block/pblk/pblk/write_amp_mileage") as f:
        write_amp = f.read()

    with open("/sys/block/pblk/pblk/rate_limiter") as f:
        rate_limiter = f.read()

    for e in gc_state.split(","):
        ret.append(int(e.split('=')[1]))

    write_amp_dic = {}
    for e in write_amp.split(" "):
        k, v = e.split(":")
        write_amp_dic[k] = v


    ret.append(int(write_amp_dic['user']))
    ret.append(int(write_amp_dic['gc']))
    ret.append(float(write_amp_dic['WA']))

    tmp = p_rate_limiter_user.match(rate_limiter)
    limiter_u_a, limiter_u_b =

    return ret


def waitGCComplete():
    while True:
        time.sleep(0.3)
        g = _getGCLog()
        gc_active = g[1]

        if gc_active == 0:
            time.sleep(5)
            return


def collectGCLog(dev, dataDir, jobName, runTime, waitTime = 300):
    pid = os.fork()
    if pid != 0:
        return pid

    time.sleep(waitTime)

    print("\033[0;34m Starting GC Log collection, time: %s \033[0m" % (time.time()))

    startTime = time.time()
    targetFile = os.path.join(dataDir, "%s-GCLog-%s" % (jobName, startTime))

    with open(targetFile, 'w') as f:
        while time.time() < startTime + float(runTime):
            acquire_time = time.time()
            record = _getGCLog()
            f.write("%f, %s, %s, %s, %s, %s\n" % (acquire_time - startTime, *record))

            f.flush()
            # time.sleep(0.001)

    print("\033[0;34m GC collection complete \033[0m")
    exit(0)
