#!/usr/bin/env python3

import os
import subprocess
import logging
import logging.config
import yaml
import shlex


logging.config.dictConfig(yaml.safe_load("""
    version: 1
    formatters:
      file:
        format: '%(asctime)s %(levelname)s: %(message)s'
      console:
        format: '########## %(asctime)s %(levelname)s: %(message)s'
    handlers:
      file:
        class: logging.FileHandler
        formatter: file
        filename: builder.log
        level: DEBUG
      console:
        class: logging.StreamHandler
        formatter: console
        stream: ext://sys.stdout
        level: INFO
    root:
      level: DEBUG
      handlers: [file, console]
    """))

log = logging.getLogger(__name__)


def call(command):
    # command = command.format_map(users)
    log.debug("executing %s", command)
    return subprocess.call(shlex.split(command))


def check_call(command):
    # command = command.format_map(users)
    log.debug("executing %s", command)
    subprocess.check_call(shlex.split(command))


def check_output(command):
    command = command.format_map(users)
    log.debug("executing %s", command)
    return subprocess.check_output(shlex.split(command),
                                   universal_newlines=True)


