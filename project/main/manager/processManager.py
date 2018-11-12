#!/usr/bin/env python
# -*- coding: utf-8 -*-

#
# get the count of the process:
#  ps -ef|grep "python3 -m ipykernel_launcher"|wc -l
#
# get all the pIds of the parent process:
#   ps -ef |grep parent_proc|egrep -v grep | awk '{print $2}'
#   eg: ps -ef |grep 28568|egrep -v grep | awk '{print $2}'
#
#

# def autoCleanProcess():
#
#     cmd =
#
#     pass