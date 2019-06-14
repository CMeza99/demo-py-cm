"""cm
Config Management POC

Usage:
  cm STATE [HOSTNAMES...]
  cm (-h | --help)
  cm (-v | --version)

Options:
  -v --version                  Show version
  -h --help                     Show this screen
"""

import logging
import socket

from typing import Optional

import pkg_resources

from docopt import docopt
import paramiko

from .base import Host, Runner, state


version: Optional[str] = None
logging.basicConfig(level=logging.DEBUG)
_LOG = logging.getLogger(__name__)

try:
    version = pkg_resources.get_distribution(__package__).version
except pkg_resources.DistributionNotFound:
    version = None


def main():
    arguments = docopt(__doc__, version=version, options_first=False)
    _LOG.debug("Arguments received: %s", arguments)

    runner = Runner()
    hosts = []

    for host in arguments.get("HOSTNAMES", []):
        try:
            h = Host(host)
        except (paramiko.ssh_exception.SSHException, socket.error) as err:
            _LOG.error("Failed creating Host(\"%s\"): %s", host, err)
            # TODO
            pass
        else:
            hosts.append(h)
        finally:
            h = None

    runner.addhosts(hosts)
    _LOG.debug("Runner: %s", runner)
    states = {}  # should probable be a set
    states["apache"] = state.Pkg("apache2")
    for host in runner.hosts:
        host.states.append(states["apache"])
    runner.run()
    print(runner)


if __name__ == "__main__":
    main()
