#!/usr/bin/env python3

import os
import subprocess
import docker

from _common import *
from _config import *

from SC import *

BASE_IMAGE = "debian:13-slim"
BUILD_ENV = ["DEBIAN_FRONTEND=noninteractive","SNORG=tees"]

builder = SCImageBuilder(BASE_IMAGE)

###
#    filelist is defined in _config
#
#    The packages listed in the file(s) will be installage at the given level
###
for file in filelist:
    spud, level, filename = file.split('/')
    builder.add_file(level, file)

builder.client = docker.from_env()
cid = builder.create(BUILD_ENV)


command = "apt update"
builder.exec(cid, command)
command = "apt upgrade -y"
builder.exec(cid, command)
command = "apt install -y less vim"
builder.exec(cid, command)
exit()

