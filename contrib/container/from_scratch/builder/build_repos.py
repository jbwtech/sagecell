#!/usr/bin/env python3

import os
import subprocess
from build_common import *

# GitHub repositories
repositories = [
    ("sagemath", "sage", "master"),
    ("sagemath", "sagecell", "master"),
]

def update_repositories():
    # Clone/update repositories and checkout appropriate branches.
    if not os.path.exists("github"):
        os.mkdir("github")
    os.chdir("github")
    git = lambda command: check_call("git " + command)
    for user, repository, branch in repositories:
        log.info("updating repository %s", repository)
        if not os.path.exists(repository):
            git("clone https://github.com/{}/{}.git".format(user, repository))
        os.chdir(repository)
        git("fetch")
        git("checkout " + branch)
        if call("git symbolic-ref -q HEAD") == 0:
            git("pull")
        os.chdir(os.pardir)
    os.chdir(os.pardir)


