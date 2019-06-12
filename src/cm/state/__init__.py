""" Package cm.state top level """
from abc import ABCMeta, abstractmethod
from dataclasses import dataclass, field
from typing import Optional
import logging


_LOG = logging.getLogger(__name__)

@dataclass
class State(metaclass=ABCMeta):
    name: str = field()
    modified: bool = field(default=False, init=False)
    exitcode: Optional[int] = field(default=None, init=False)
    error: Optional[str] = field(default=None, init=False)
    # client: Optional = field(default=None)

    @abstractmethod
    def run(self, host):
        pass


class Pkg(State):

    def _cmd(self, host, subcommand="install"):
        _LOG.debug("%s %s on %s", subcommand, self.name, host.name)
        _, stdout, stderr = host.runcmd(f"apt-get -qq update")
        _, stdout, stderr = host.runcmd(f"apt-get -qq {subcommand} -y {self.name}")
        # TODO: Remove blocking for exit code
        self.exitcode = stdout.channel.recv_exit_status()
        self.error = stderr.readlines()
        return self.exitcode

    def isinstalled(self, host):
        _LOG.debug("Checking if %s is installed on %s", self.name, host.name)
        _, stdout, _ = host.runcmd(f"dpkg -l {self.name} | grep -E '^ii *{self.name} '")
        status = not stdout.channel.recv_exit_status()
        return status

    def install(self, host):
        # TODO cache running `apt-get update`
        self._cmd(host, "install")

    def run(self, host):
        if not self.isinstalled(host):
            if self.install(host) == 0:
                self.modified = True
        else:
            self.exitcode = 0
        return self.exitcode
