import argparse
from fabric import Connection
from invoke import Responder
import GPUtil as GPU

hosts = ['torrnode1', 'torrnode2', 'torrnode3', 'torrnode4', 'torrnode5', 'torrnode6', 'torrnode7', 'torrnode8']

parser = argparse.ArgumentParser(description='GPU Scheduler')
parser.add_argument("--num_gpu", type=int, help="specify number of GPUs needed")
parser.add_argument("--memory_per_gpu", type=int, help="specify free per gpu memory requirement in GB")

args = parser.parse_args()


def main():
    for host in hosts:
        host_connect = Connection(hosts)
        host_connect.run('python /homes/55/adel/test/test_write_disk.py')
        GB = 1024
        gpu_IDs = []
        GPUs = GPU.getGPUs()
        for i in range(len(GPUs)):
            if args.num_gpu >= len(gpu_IDs):
                gpu = GPUs[i]
                if (gpu.load*100.0 < 20.0) and (gpu.memoryUtil*100 <= 10.0) and (gpu.memoryFree/GB >= args.memory_per_gpu):
                    print("GPU RAM Free: {0:.0f}MB | Used: {1:.0f}MB | Util {2:3.0f}% | Total {3:.0f}MB".format(gpu.memoryFree, gpu.memoryUsed, gpu.memoryUtil*100, gpu.memoryTotal))
                    # print(gpu.load)
                    gpu_IDs.append(i)
        print(gpu_IDs)


if __name__ == "__main__":
    main()


# >>> from fabric import Connection
# >>> result = Connection('web1.example.com').run('uname -s', hide=True)
# >>> msg = "Ran {0.command!r} on {0.connection.host}, got stdout:\n{0.stdout}"
# >>> print(msg.format(result))
# Ran 'uname -s' on web1.example.com, got stdout:
# Linux