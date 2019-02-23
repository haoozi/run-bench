#!/usr/bin/env python3

import json
import os

"""

[

    {"name" : "Job1",
    "script" : "Jobs/Job1.sh",
    "wait_time_before_collect" : 300,
    "runtime" : "1000" or "timebased"}
]


"""


class Jobs(object):
    """docstring for Jobs."""
    def __init__(self, joblist = "job.json"):
        with open(joblist) as f:
            self.jobs = json.load(f)

    def getJobList(self):
        return self.jobs

    def forEachJob(self, func):
        for eachjob in self.jobs:
            func()
