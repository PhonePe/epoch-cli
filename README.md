# Epoch CLI

Command line interface for the Epoch Container Orchestrator.

# Getting Started

## Installation

You can install the cli from from PyPI.

```bash
pip install epoch-cli
```

Reactivate/deactivate virtual environment based on the need to utilize epoch cli.  
Refer [dev setup](#Setting-up-virtual-environment) on how to setup virtual environment and install epoch-cli.

## Running using docker

The cli is pushed as a docker for easy access. This also elimintates the need for having python etc setup on your
system.

1) Pull the image:

```shell
docker pull ghcr.io/phonepe/epoch-cli:latest
```

2) Create a shell script called `epoch` with the following content:

```shell
#! /bin/sh
docker run \
    --rm --interactive --tty --network host \
    --name epoch-cli -v ${HOME}/.epoch:/root/.epoch:ro  \
    ghcr.io/phonepe/epoch-cli:latest "$@"

```

3) Make the script executable

```shell
chmod a+x epoch
```

4) Put the path to this script in your `~/.bashrc`.

```shell
export PATH="${PATH}:/path/to/your/script"
```

5) Logout/login or run `. ~/.bashrc` to load the new [path]


6) Run epoch cli

```
epoch -h
```

## Requirements

The CLI is written in Python 3x

## Accessing the Documentation

The arguments needed by the script are self documenting. Please use `-h` or `--help` in different sections and
sub-sections of the CLI to get descriptions of commands, sub-commands, their arguments and options.

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

In order to use the CLI, we need to provide coordinates to the cluster to connect to. This can be done in the following
manner:

## Epoch CLI config file

The config file can be located in the following paths:

* `.epoch` file in your home directory (Typically used for the default cluster you frequently connect to)
* A file in any path that can be passed as a parameter to the CLI with the `-f FILE` option

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

The `DEFAULT` section can be used to define common variables like Insecure etc. The `local`, `stage`, `production` etc
are names for inidividual clusters and these sections can be used to define configuration for individual clusters.
Cluster name is referred to in the command line by using the `-c` command line option.\
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
* If a value is provided in the `auth_header` parameter, it is passed as the value for the `Authorization` header in the
  upstream HTTP calls to the Epoch server verbatim.
* If neither, no auth is set

> NOTE: Use the `insecure` option to skip certificate checks on the server endpoint (comes in handy for internal
> domains)

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

This will connect to the cluster whose config is mentioned in the `[stage]` config section in `$HOME/.epoch` config
file.

## Command line options

Pass the endpoint and other options using `--endpoint|-e` etc etc. Options can be obtained using `-h` as mentioned
above. Invocation will be in the form:

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
epoch topology get [-h] topology-id
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

##### pause-all

Pause all topologies for cluster

```
epoch cluster pause-all
```

##### import

Import topologies for cluster

```
epoch cluster import [-h] file_name
```

###### Positional Arguments

`file_name` - Name of file to be imported

`--overwrite` True/False - Overwrite topologies that already exist (default: False)

`--paused` True/False- Pause all jobs while importing (default: False)

`--skip`- Comma seperated list of jobs to be skipped (default: "")

##### export

Export topologies for cluster

```
epoch cluster export [-h] file_name
```

###### Positional Arguments

`file_name` - Name of file to be saved

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
epoch runs kill [-h] topology-id run-id task-name
```

###### Positional Arguments

`topology-id` - Topology-id
`run-id` - Run-id
`task-name` - Task-name to be killed

##### log

gets the log the given taskid.

```
epoch runs log [-h] topology-id run-id task-name
```

###### Positional Arguments

`topology-id` - Topology-id
`run-id` - Run-id
`task-name` - Task-name to be fetched

## Setting-up virtual environment
```
python3 -m venv testingEpochCli
cd testingEpochCli
source bin/activate
pip install epoch-cli
```
Move the setting.ini to the testingEpochCli directory and add auth tokens/username/passwords along with valid environments for different epoch endpoints.
```
epoch -f setting.ini -c env runs list job_name
```

©2024, Shubhransh Jagota.