# GPU scheduler for Torr nodes
GPU scheduler over torr nodes

## Installation

### SSH connection

Add the following to `~/ssh/config`:

```
Host torrnode1
   HostName torrnode1.robots.ox.ac.uk
   User [USER]
Host torrnode2
   HostName torrnode2.robots.ox.ac.uk
   User [USER]
Host torrnode3
   HostName torrnode3.robots.ox.ac.uk
   User [USER]
Host torrnode4
   HostName torrnode4.robots.ox.ac.uk
   User [USER]
Host torrnode5
   HostName torrnode5.robots.ox.ac.uk
   User [USER]
Host torrnode6
   HostName torrnode6.robots.ox.ac.uk
   User [USER]
Host torrnode7
   HostName torrnode7.robots.ox.ac.uk
   User [USER]
Host torrnode8
   HostName torrnode8.robots.ox.ac.uk
   User [USER]
```

where `[USER]` is your `robots.ox.ac.uk` username.

### Python package

Clone this repo in the cluster and install it by running:

``` 
cd gpu_scheduler
pip install .
```

Repeat these steps within your local environment. You should be good to go!

## Usage

To get list of all free GPUs on all nodes:

```
torrnodes_free_gpus
```

If you need a GPU with a certain minimum memory `M`, run this command to find out the free ones that satisfy it:

```
torrnodes_free_gpus -m M
```

To run a batch of jobs, run:

```
torrnodes_run_commands -c [COMMAND_1] -c [COMMAND_2] ...
```

Run `torrnodes_run_commands -h` for help.