# Demo: Py Config Managment

cli tool to run apply states defined in toml, yaml, or json files.

## Usage

```sh
Config Management POC

Usage:
  cm STATE [HOSTNAMES...]
  cm (-h | --help)
  cm (-v | --version)

Options:
  -v --version                  Show version
  -h --help                     Show this screen
```

### Note

* Add this time the modules to read in states are not implemented. There is a hardcoded example of the `Package` state in `cli.py`.
* A basic CI/CD framework was started. Here is where the intergration tests would go https://dev.azure.com/cmeza99/demo-cm/_build/results?buildId=3&view=logs&jobId=0389ffc6-891d-503d-bdd5-1876bc6c680e&taskId=827cbc67-49dc-56e9-4043-713c77bb2f19&lineStart=145&lineEnd=146&colStart=1&colEnd=1

## To Do

* [ ] TestInfra for integration tests and deployment verification
* [ ] Modules to read in state configuration
* [ ] Have ssh keys generated on the fly in CI
* [ ] Configuration for hosts, i.e. keys, passphases, user, etc
* [ ] Make tests pass :)
