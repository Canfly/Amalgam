# amctl

> Amalgam Command Line Tools

For more information see: https://github.com/Canfly/Amalgam

Amalgam is the Media dimension for Interactive interactions 

## Usage

```
  amctl - Amalgam Command Line Tools.

  amctl [<flags>] <command> [<arg>] ...

SUBCOMMANDS
  BASIC COMMANDS
    init          Initialize local node
    add  <object> Add a object to Amalgam

  ADVANCED COMMANDS
    daemon        Start a daemon process
    name <name>   Resolve or publish any type of name from ANS

  NETWORK COMMANDS
    id            Show info about nodeof a connection
    diag          Print diagnostics

  TOOL COMMANDS
    config        Manage configuration
    version       Show amctl version information
    commands      List all available commands

  Use 'amctl help <command> ' to learn more about each command.

  Amalgam uses a system disk. By default, the repo is located  at ~/.am
  To change the repo location, set the $AMPATH environment variable:

  bash: export AMPATH=/path/to/repo
  fish: set -gx AMPATH "/path/to/repo"
```
