#!/usr/bin/env python3

import sys
import os
import subprocess

system_packages = []


filelist = [
    "lists/addons/Rscript.txt",
    "lists/addons/sage-pip.txt",
    "lists/base/optional.txt",
    "lists/base/R.txt",
]

def load_list(path, target):
    with open(path, 'r') as file:
        for line in file:
            target.append(line.strip())

for list in filelist:
    load_list(list, system_packages)

cmd = ["apt", "install", "-y"] 

for pkg in system_packages:
    if pkg[0:1] != "#":
        cmd.append(pkg)


os.environ['DEBIAN_FRONTEND']='noninteractive'

subprocess.run(cmd, check=True)

