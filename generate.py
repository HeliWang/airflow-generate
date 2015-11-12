#!/usr/bin/env python
import sys
import os

from optparse import OptionParser
from crontab import CronTab


def main():
    parser = OptionParser()
    parser.add_option("-d", "--directory", dest="directory",
                      help="directory for output files")
    parser.add_option("-f", "--force",
                      action="store_true", dest="force", default=False,
                      help="force file overwrite")

    (options, args) = parser.parse_args()

    for cron in [CronTab(tabfile=os.path.abspath(arg)) for arg in args]:
        for job in cron:
            print(job)

    return 0

if __name__ == '__main__':
    sys.exit(main())
