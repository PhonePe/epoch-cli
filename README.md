# Epoch CLI

Command line interface for the Epoch Container Orchestrator.

# Getting Started

## Installation

### Create Virtual Environment

```bash
VENV_BASE_DIRECTORY=/path/to/base/directory/for/virtual/env
cd ${VENV_BASE_DIRECTORY}
python3 -m venv epoch_cli
```

### Activate Virtual Environment

```bash
cd ${VENV_BASE_DIRECTORY}/epoch_cli
source bin/activate
```

### Install or Upgrade epoch_cli using Pip

```bash
# For installing/upgrading to latest snapshot version
pip3 install --index https://artifactory.phonepe.com/repository/pypi-snapshots/simple --extra-index-url https://artifactory.phonepe.com/repository/pypi-org/simple --ignore-installed --force-reinstall --no-cache-dir com.phonepe.infra.epoch_cli

# For installing/upgrading to latest release version
pip3 install --index https://artifactory.phonepe.com/repository/pypi-releases/simple --extra-index-url https://artifactory.phonepe.com/repository/pypi-org/simple com.phonepe.infra.epoch_cli
```

After installation `epoch` command can be used as per user guide provided below. Once usage of `epoch` is done, virtual environment can be deactivated.

### Deactivate Virtual Environment

```bash
deactivate
```

Reactivate/deactivate virtual environment based on the need to utilize epoch cli.

## Requirements
The CLI is written in Python 3x


## Accessing the Documentation
The arguments needed by the script are self documenting. Please use `-h` or `--help` in different sections and sub-sections of the CLI to get descriptions of commands, sub-commands, their arguments and options.

To see basic help:
```

$ epoch -h

usage: epoch [-h] [--file FILE] [--cluster CLUSTER] [--endpoint ENDPOINT] [--auth-header AUTH_HEADER] [--insecure INSECURE] [--username USERNAME] [--password PASSWORD] [--debug]
             {cluster,runs,topology} ...

positional arguments:
  {cluster,runs,topology}
                        Available plugins
    cluster             Epoch cluster related commands
    runs                Epoch runs related commands
    topology            Epoch topology related commands

options:
  -h, --help            show this help message and exit
  --file FILE, -f FILE  Configuration file for epoch client
  --cluster CLUSTER, -c CLUSTER
                        Cluster name as specified in config file
  --endpoint ENDPOINT, -e ENDPOINT
                        Epoch endpoint. (For example: https://epoch.test.com)
  --auth-header AUTH_HEADER, -t AUTH_HEADER
                        Authorization header value for the provided epoch endpoint
  --insecure INSECURE, -i INSECURE
                        Do not verify SSL cert for server
  --username USERNAME, -u USERNAME
                        Epoch cluster username
  --password PASSWORD, -p PASSWORD
                        Epoch cluster password
  --debug, -d           Print details of errors

```

# Connecting to the Epoch cluster

In order to use the CLI, we need to provide coordinates to the cluster to connect to. This can be done in the following manner:

## Epoch CLI config file
The config file can be located in the following paths:
* `.epoch` file in your home directory (Typically used for the default cluster you frequently connect to)
*  A file in any path that can be passed as a parameter to the CLI with the `-f FILE` option

### Config File format
This file is in ini format and is arranged in sections.

```ini
[DEFAULT]
...
stage_token = <token1>
prod_token = <token2>

[local]
endpoint = http://localhost:10000
username = admin
password = admin

[stage]
endpoint = https://stage.testepoch.io
auth_header = %(stage_token)s

[production]
endpoint = https://prod.testepoch.io
auth_header = %(prod_token)s

..
```

The `DEFAULT` section can be used to define common variables like Insecure etc. The `local`, `stage`, `production` etc are names for inidividual clusters and these sections can be used to define configuration for individual clusters. Cluster name is referred to in the command line by using the `-c` command line option.\
*Interpolation* of values is supported and can be acieved by using `%(variable_name)s` references.

> * Note: The `DEFAULT` section is mandatory
> * Note: The `s` at the end of `%(var)s` is mandatory for interpolation

### Contents of a Section
```
endpoint = https://yourcluster.yourdomain.com # Endpoint for cluster
insecure = true
username = <your_username>
password = <your_password>
auth_header= <Authorization value here if using header based auth>
```

Authentication priority:
* If both `username` and `password` are provided, basic auth is used.
* If a value is provided in the `auth_header` parameter, it is passed as the value for the `Authorization` header in the upstream HTTP calls to the Epoch server verbatim.
* If neither, no auth is set

> NOTE: Use the `insecure` option to skip certificate checks on the server endpoint (comes in handy for internal domains)

To use a custom config file, invoke epoch in the following form:

```
$ epoch -f custom.conf ...
```

This will connect to the cluster if an endpoint is mentioned in the `DEFAULT` section.

```
$ epoch -f custom.conf -c stage ...
```

This will connect to the cluster whose config is mentioned in the `[stage]` config section.

```
$ epoch -c stage ...
```

This will connect to the cluster whose config is mentioned in the `[stage]` config section in `$HOME/.epoch` config file.


## Command line options
Pass the endpoint and other options using `--endpoint|-e` etc etc. Options can be obtained using `-h` as mentioned above. Invocation will be in the form:

```
$ epoch -e http://localhost:10000 -u guest -p guest ...
```

## CLI format
The following cli format is followed:

```
usage: epoch [-h] [--file FILE] [--cluster CLUSTER] [--endpoint ENDPOINT] [--auth-header AUTH_HEADER] [--insecure INSECURE] [--username USERNAME] [--password PASSWORD] [--debug]
             {cluster,runs,topology} ...
```
### Basic Arguments
```
  -h, --help            show this help message and exit
  --file FILE, -f FILE  Configuration file for epoch client
  --cluster CLUSTER, -c CLUSTER
                        Cluster name as specified in config file
  --endpoint ENDPOINT, -e ENDPOINT
                        Epoch endpoint. (For example: https://epoch.test.com)
  --auth-header AUTH_HEADER, -t AUTH_HEADER
                        Authorization header value for the provided epoch endpoint
  --insecure INSECURE, -i INSECURE
                        Do not verify SSL cert for server
  --username USERNAME, -u USERNAME
                        Epoch cluster username
  --password PASSWORD, -p PASSWORD
                        Epoch cluster password
  --debug, -d           Print details of errors

```

## Commands
Commands in epoch are meant to address specific functionality. They can be summarized as follows:
```
    cluster             Epoch cluster related commands
    runs                Epoch runs related commands
    topology            Epoch topology related commands
```
---
 Topology
---
Epoch topology executor related commands

```
epoch topology [-h] {list,get,create,update,delete,pause,unpause,run} ...
```

#### Sub-commands

##### list

List all executors

```
epoch topology list [-h]
```

##### get

Show details about topology-id

```
drove topology get [-h] topology-id
```

###### Positional Arguments

`topology-id` - Topology-id to be shown

##### run

Run the given topology-id

```
epoch topology run [-h] topology-id
```
###### Positional Arguments

`topology-id` - Topology-id to be run

##### create

Create a task on cluster
```
epoch topology create [-h] spec-file
```
###### Positional Arguments

`spec-file` - JSON spec file for the topology

##### update

Update topology running on this cluster

```
epoch topology update [-h] spec-file
```

###### Positional Arguments

`spec-file` - JSON spec file for the topology

##### pause

Pause the given topology-id

```
epoch topology pause [-h] topology-id
```
###### Positional Arguments

`topology-id` - Topology-id to be paused

##### unpause

Unpause the given topology-id

```
epoch topology unpause [-h] topology-id
```
###### Positional Arguments

`topology-id` - Topology-id to be unpaused

##### delete

Delete the given topology-id

```
epoch topology delete [-h] topology-id
```
###### Positional Arguments

`topology-id` - Topology-id to be deleted

---

Cluster
---
Epoch cluster related commands

```
epoch cluster [-h] {leader} ...
```

#### Sub-commands


##### leader

Show leader for cluster
```
epoch cluster leader [-h]
```

---

Runs
---
Epoch application related commands

```
epoch runs [-h] {list,get,kill,log} ...
```
#### Sub-commands

##### list

List all runs

```
epoch runs list [-h]
```

##### get

get the details for the given Topology's runId
```
epoch runs get [-h] topology-id run-id
```
###### Positional Arguments

`topology-id` - Topology-id
`run-id` - Run-id to be fetched

##### kill

Kills the given taskid.
```
epoch runs kill [-h] topology-id run-id task-id
```
###### Positional Arguments

`topology-id` - Topology-id 
`run-id` - Run-id 
`task-id` - Task-id to be killed

##### log

gets the log the given taskid.
```
epoch runs log [-h] topology-id run-id task-id
```
###### Positional Arguments

`topology-id` - Topology-id 
`run-id` - Run-id 
`task-id` - Task-id to be fetched


©2024, Shubhransh Jagota.