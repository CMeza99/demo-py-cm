""" """
import socket
import logging
import time

from dataclasses import dataclass, field
from typing import Dict, FrozenSet, Iterable, List, Optional, Set

import paramiko

from cm.helper import Singleton
from cm import state

paramiko.util.log_to_file("ssh.log")
logging.basicConfig(level=logging.DEBUG)
_LOG = logging.getLogger(__name__)


@dataclass(eq=False)
class Runner(metaclass=Singleton):
    hosts: Iterable = field(default_factory=set)

    def __post_init__(self):
        self.hosts = set(self.hosts)

    def addhosts(self, hosts: Iterable):
        self.hosts.update(hosts)

    def rmhosts(self, hosts: Iterable):
        self.hosts.difference_update(hosts)
        return self.hosts

    def gethost(self, hostname):
        for host in self.hosts:
            if host.name == hostname:
                return host
        return None

    def run(self):

        for host in self.hosts:
            _LOG.debug("Running host %s", host.name)
            host.runstates()


@dataclass(unsafe_hash=True)
class Host:
    name: str = field(compare=True, repr=True)
    username: Optional[str] = field(default=None, compare=False, repr=False)
    password: Optional[str] = field(default=None, compare=False, repr=False)
    key: Optional[str] = field(default=None, compare=False, repr=False)
    states: List = field(default_factory=list, compare=False, repr=True)
    ssh: paramiko.client = field(default=paramiko.SSHClient(), init=False, compare=False, repr=False)

    def __post_init__(self):
        self.ssh.load_system_host_keys()  # pylint: disable=no-member
        self.ssh.set_missing_host_key_policy(paramiko.WarningPolicy())  # pylint: disable=no-member
        self.ssh.connect(  # pylint: disable=no-member
            hostname=self.name,
            username=self.username,
            gss_auth=paramiko.GSS_AUTH_AVAILABLE,
            gss_kex=paramiko.GSS_AUTH_AVAILABLE,
        )

    def runcmd(self, cmd: Optional[str] = None):
        """
        Blocking run
        Has several pitfalls including:
        - buffer filling up
        - server may not return an exit status
        """
        data = self.ssh.exec_command(cmd)  # pylint: disable=no-member
        while not data[1].channel.exit_status_ready():
            # TODO: read stdin and error rather than potentially letting the buffer fill up
            time.sleep(1)

        return data

    def runstates(self):
        # TODO: Order states
        # Pkg, files, services
        for s in self.states:
            s.run(self)
