#!/usr/bin/env python3

import os
import sys
import time
import signal





import util
import job



dev = "/dev/pblk"
dataDir = "./data"

j = job.Jobs()



jobs = j.getJobList()

print("Parsed Jobs:")
print(jobs)


#
# def wait_child(signum, frame):
#     logging.info('receive SIGCHLD')
#     try:
#         cpid, status = os.waitpid(-1, os.WNOHANG)
#     except OSError as e:
#         print(e)
#     logging.info('handle SIGCHLD end')
#
# signal.signal(signal.SIGCHLD, wait_child)
#





for eachJob in jobs:
    print("Job config:")
    print(eachJob)
    time.sleep(1)
    print("Start filling SSD, start time %s" % (time.time()))
    util.fillSSD()

    print("Start %s, script %s" % (eachJob["name"], eachJob["script"]))

    waitTime = eachJob["wait_time_before_collect"]
    runTime = eachJob["runtime"] if eachJob["runtime"] != "timebased" else 99999


    pid_gc = util.collectGCLog(dev, dataDir, eachJob["name"], runTime, waitTime)

    pid_blktrace = util.collectBlkTrace(dev, dataDir, eachJob["name"], runTime, waitTime)



    ret = util.run_and_get_result(["sh", eachJob["script"]])
    print("Job %s complete" % (eachJob["name"]))



    try:
        os.waitpid(-1, os.WNOHANG)
        os.kill(pid_gc, signal.SIGINT)
    except:
        print("GC State Collection finished")
    else:
        print("GC State Collection is running, kill...")



    try:
        os.waitpid(-1, os.WNOHANG)
        os.kill(pid_blktrace, signal.SIGINT)
    except:
        print("Blktrace finished")
    else:
        print("Blktrace is running, kill...")

    time.sleep(10)

print("All done")
