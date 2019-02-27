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
    print("\033[0;31m Job config:\033[0m")
    print(eachJob)
    time.sleep(1)
    print("\n\033[0;31m Start filling SSD, start time %s\033[0m\n" % (time.time()))
    util.fillSSD()
    print("\033[0;31m SSD Filling complete\033[0m\n")




    print("\033[0;31m Waiting for GC complete\033[0m\n")
    util.waitGCComplete()
    print("\033[0;31m GC completed, continue...\033[0m\n")


    print("\033[0;31m Start %s, script %s\033[0m\n" % (eachJob["name"], eachJob["script"]))

    waitTime = eachJob["wait_time_before_collect"]
    runTime = eachJob["runtime"] if eachJob["runtime"] != "timebased" else 99999

    #
    # pid_gc = util.collectGCLog(dev, dataDir, eachJob["name"], runTime - waitTime, waitTime)
    #
    # pid_blktrace = util.collectBlkTrace(dev, dataDir, eachJob["name"], runTime - waitTime, waitTime)



    pid_gc = util.collectGCLog(dev, dataDir, eachJob["name"], runTime, 0)

    pid_blktrace = util.collectBlkTrace(dev, dataDir, eachJob["name"], runTime, 0)


    # ret = util.run_and_get_result(["sh", eachJob["script"]])

    util.run_direct("sh %s" % eachJob["script"])
    print("\033[0;31m Job %s complete \033[0m\n" % (eachJob["name"]))



    os.kill(pid_gc, signal.SIGTERM)

    os.kill(pid_blktrace, signal.SIGTERM)

    time.sleep(10)

    try:
        os.waitpid(-1, os.WNOHANG)
    except:
        pass


print("\033[0;31m All done \033[0m")
