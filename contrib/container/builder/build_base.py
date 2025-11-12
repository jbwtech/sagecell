#!/usr/bin/env python3

import os
import subprocess


# Theses are the lists of packages to install
filelist = [
    "lists/base/prerequisites.txt",
    "lists/base/recommended.txt",
    "lists/base/optional.txt",
    "lists/base/R.txt",
    "lists/R/Rscript.txt",
]

packages = []

for filename in filelist:
    with open(filename, 'r') as file:
        rootdir, target, path = filename.split("/")
        for line in file:
            if line[0] != "#":
                dict = {"level": target, "package": line.strip()}
                packages.append(dict)

install_list = ""

cmd = ["apt", "install", "-y", "--no-install-recommends"]

for pkg in packages:
    if pkg['level'] == 'base':
        package = pkg['package']
        install_list += package + " "
        cmd.append(package)

subprocess.run(cmd, check=True)

for pkg in packages:
    if pkg['level'] == 'R':
        package = pkg['package']
        command = ["Rscript", "-e", f"install.packages(\"{package}\")" ]
        subprocess.run(command)

