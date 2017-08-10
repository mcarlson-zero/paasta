#!/usr/bin/env python
# Copyright 2015-2016 Yelp Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
import argparse
import sys

from paasta_tools.mesos.exceptions import MasterNotAvailableException
from paasta_tools.mesos_tools import get_mesos_master
from paasta_tools.metrics.metastatus_lib import assert_no_duplicate_frameworks
from paasta_tools.utils import paasta_print


def parse_args():
    parser = argparse.ArgumentParser()

    parser.add_argument(
        '--ignore', '-i', dest='ignore', type=str, default='',
        help='Comma separated list of frameworks to ignore',
    )


def check_mesos_no_duplicate_frameworks():
    options = parse_args()
    ignore = options.ignore.split(',')
    master = get_mesos_master()
    try:
        state = master.state
    except MasterNotAvailableException as e:
        paasta_print("CRITICAL: %s" % e.message)
        sys.exit(2)

    result = assert_no_duplicate_frameworks(state, ignore=ignore)
    if result.healthy:
        paasta_print("OK: " + result.message)
        sys.exit(0)
    else:
        paasta_print(result.message)
        sys.exit(2)


if __name__ == '__main__':
    check_mesos_no_duplicate_frameworks()