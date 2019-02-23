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




for eachJob in jobs:
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
        os.kill(pid_gc, signal.SIGINT)
    except ProcessLookupError as e:
        print("GC State Collection finished")
    else:
        print("GC State Collection is running, kill...")



    try:
        os.kill(pid_blktrace, signal.SIGINT)
    except ProcessLookupError as e:
        print("Blktrace finished")
    else:
        print("Blktrace is running, kill...")

    time.sleep(10)

print("All done")
