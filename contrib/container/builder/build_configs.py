#!/usr/bin/env python3

import os
import subprocess
from build_common import *

# limits configuration for the host - will not be overwritten later
limits_conf = """\
* - nofile 32768
root - nofile 32768
"""

# rsyslog configuration for the host - will not be overwritten later
rsyslog_conf = r"""global(maxMessageSize="64k")

module(load="imrelp")
input(type="imrelp" port="12514")

template(name="sagecell" type="list") {
    property(name="hostname")
    constant(value=" ")
    property(name="syslogtag")
    property(name="msg" spifno1stsp="on")
    property(name="msg" droplastlf="on")
    constant(value="\n")
    }

if $syslogfacility-text == "local3" then
    {
    action(type="omfile"
           file="/var/log/sagecell.stats.log"
           template="sagecell")
    stop
    }
"""

def run_it():
    # Do it only once and let users change it later.
    if not os.path.exists("/etc/security/limits.d/sagecell.conf"):
        log.info("setting up security limits configuration file")
        with open("/etc/security/limits.d/sagecell.conf", "w") as f:
            f.write(limits_conf)
        log.info("Finish this session and start a new one for system configuration"
                 " changes to take effect.")
        exit()

    if not os.path.exists("/etc/rsyslog.d/sagecell.conf"):
        log.info("setting up rsyslog configuration file")
        with open("/etc/rsyslog.d/sagecell.conf", "w") as f:
            f.write(rsyslog_conf)
        check_call("systemctl restart rsyslog")

