from datetime import datetime
import time
from fabric import Connection
import argparse


class GPUScheduler(object):
    def __init__(self):
        # torrnode3 > issues with password
        # torrnode6 > gpus down
        self.allhosts = [
            "torrnode1", "torrnode2", "torrnode4",
            "torrnode5", "torrnode7", "torrnode8"
        ]

    @staticmethod
    def print_with_timestamp(msg):
        timestamp = datetime.now().strftime("%d-%m-%Y, %H:%M:%S")
        print(f"{timestamp}: {msg}")

    def ping_avail_gpus(self, min_memory_per_gpu=11, sleep_time=30):
        """
            Keeps pining Torrnodes until it returns at least
            one free avialble GPU with a full list stat
        """
        print(
            f"########## Refresh List of GPUs (min memory: {min_memory_per_gpu}GB) ###########"
        )
        gpu_list = self._get_gpu_list()

        while(len(gpu_list) == 0):
            self.print_with_timestamp(
                "no available GPUs found; refreshing in {sleep_time} secs!"
            )
            time.sleep(sleep_time)
            gpu_list = self._get_gpu_list()

        for hostname, list_gpu_numbers in gpu_list.items():
            for gpu_number in list_gpu_numbers:
                self.print_with_timestamp(
                    f"available GPU: {hostname} #{gpu_number}."
                )

    def _get_crawlwer_list(self, host, min_memory_per_gpu=11):
        c = Connection(host)
        result = c.run(
            f"torr_gpu_crawler --memory_per_gpu {min_memory_per_gpu} --card_exception 'Tesla K40m'",
            hide=True
        )
        all_IDs = result.stdout.replace("[", "").replace("]","").replace("\n", ""). replace(" ", "")
        all_IDs = all_IDs.split(",")

        return all_IDs

    def _get_gpu_list(self, min_memory_per_gpu=11):
        gpu_list = {}
        for host in self.allhosts:
            all_IDs = self._get_crawlwer_list(host)
            if len(all_IDs) == 1 and all_IDs[0] == "":
                continue
            gpu_list[host] = all_IDs
        return gpu_list

    def _is_empty_list(self, all_IDS):
        if len(all_IDS) == 1 and all_IDS[0] == "":
            return -1
        else:
            return all_IDS[0]

    def get_one_gpu(self, min_memory_per_gpu=11, sleep_time=30):
        gpu_ID = -1
        while (gpu_ID == -1):
            self.print_with_timestamp("searching for a single free GPU!")
            for host in self.allhosts:
                all_IDs = self._get_crawlwer_list(host)
                gpu_ID = self._is_empty_list(all_IDs)
                if gpu_ID != -1:
                    self.print_with_timestamp(
                        f"found a GPU on {host} with ID#: {gpu_ID}"
                    )
                    break

            self.print_with_timestamp(
                f"-- failed to find one; will retry in {sleep_time} secs."
            )
            time.sleep(sleep_time)

        return host, gpu_ID

    def launch_single_job(self, hostname, my_command):
        with Connection(hostname) as c:
            c.run(my_command, hide=True, pty=False)

    def launch_job_batch(self, list_commands, dir_path=None, env_name=None):
        """
        Function takes the remote directory path and conda envirnoment name
        along with a list of commands in the form "python test.py --arg param"
        """
        self.print_with_timestamp("running a batch of commands...")

        completed_jobs = 0
        while(completed_jobs < len(list_commands)):
            # get one free GPU
            host, gpu_ID = self.get_one_gpu()
            all_str = list_commands[completed_jobs]

            final = ""
            if dir_path is not None:
                final = f"cd {dir_path} ;"

            if env_name is not None:
                final += f"conda activate {env_name} ;"

            final += f"CUDA_VISIBLE_DEVICES={gpu_ID} nohup " + all_str +\
                f" > logs/my_out{completed_jobs}.out 2>&1  &"

            self.print_with_timestamp(f"running jobs on node: {host}")
            print(final)

            self.launch_single_job(host, final)
            completed_jobs += 1


def avail_gpus():
    parser = argparse.ArgumentParser(description="Ping available GPUs")
    parser.add_argument(
        "-m",
        "--min-mem",
        type=float,
        default=11.0,
        help="minimum memory (in GB) for the free GPUs"
    )
    args = parser.parse_args()

    GPUScheduler().ping_avail_gpus(min_memory_per_gpu=args.min_mem)


def run_commands():
    parser = argparse.ArgumentParser(description="GPU Scheduler")
    parser.add_argument(
        "-c",
        "--commands",
        type=str,
        nargs="+",
        required=True,
        help="commands to run"
    )
    parser.add_argument(
        "-d",
        "--dir-path",
        type=str,
        help="directory where commands are to be run"
    )
    parser.add_argument(
        "-e",
        "--conda-env",
        type=str,
        help="conda environment in which to run commands"
    )
    args = parser.parse_args()

    GPUScheduler().launch_job_batch(
        list_commands=args.commands,
        dir_path=args.dir_path,
        env_name=args.conda_env
    )
