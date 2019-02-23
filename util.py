#! /usr/bin/env python3

import os
import time
import os.path


def run_and_get_result(param, print_param = True):
    if print_param:
        print(param)
    ret = subprocess.check_output(param)
    # return int(re.sub("[a-z]", '', strTime))
    s = ret.decode('utf-8')
    return s

def fillSSD():
    cmd = ["sh", "Jobs/Fill.sh"]
    ret = run_and_get_result(cmd)
    print(ret)



def fork_and_run(param, print_param = True):
    pid = os.fork()
    if pid != 0:
        return pid

    ret = run_and_get_result(param, print_param)
    print(ret)
    exit(0)


def collectBlkTrace(dev, dataDir, jobName, runTime, waitTime = 300):
    pid = os.fork()
    if pid != 0:
        return pid


    time.sleep(waitTime)
    print("Launch blktrace, time: %s" % (time.time()))


    startTime = time.time()
    targetDir = os.path.join(dataDir, "%s-blktrace-%s" % (jobName, startTime))

    ret = run_and_get_result(["blktrace", "-d", dev, "-o", targetDir, "-w", str(runTime)])
    print(ret)
    exit(0)



def _getGCLog():
    """ret : [gc_enabled, gc_active, user_write, gc_write, write_amp]"""
    gc_state = ""
    write_amp = ""
    ret = []

    with open("/sys/block/pblk/pblk/gc_state") as f:
        gc_state = f.read()

    with open("/sys/block/pblk/pblk/write_amp_mileage") as f:
        write_amp = f.read()

    for e in gc_state.split(","):
        ret.append(int(e.split('=')[1]))

    write_amp_dic = {}
    for e in write_amp.split(" "):
        k, v = e.split(":")
        write_amp_dic[k] = v


    ret.append(int(write_amp_dic['user']))
    ret.append(int(write_amp_dic['gc']))
    ret.append(float(write_amp_dic['WA']))

    return ret

def collectGCLog(dev, dataDir, jobName, runTime, waitTime = 300):
    pid = os.fork()
    if pid != 0:
        return pid

    time.sleep(waitTime)
    print("Starting GC Log collection, time: %s" % (time.time()))

    startTime = time.time()
    targetFile = os.path.join(dataDir, "%s-GCLog-%s" % (jobName, startTime))

    with open(targetFile, 'w') as f:
        while time.time() < startTime + runTime:
            acquire_time = time.time()
            record = _getGCLog()
            f.write("%s, %s, %s, %s, %s, %s\n" % (acquire_time - startTime, *record))

    exit(0)