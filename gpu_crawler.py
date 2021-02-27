import argparse
import GPUtil as GPU

parser = argparse.ArgumentParser(description='GPU Scheduler')
parser.add_argument("--memory_per_gpu", type=int, default=11, help="specify free per gpu memory requirement in GB")
parser.add_argument("--card_exception", nargs='+', type=str, default=[''], help="specify names to exclude")

args = parser.parse_args()


def main():
    GB = 1024
    gpu_IDs = []
    GPUs = GPU.getGPUs()
    for i in range(len(GPUs)):
        gpu = GPUs[i]
        if gpu.name not in args.card_exception:
            if (gpu.load*100.0 < 20.0) and (gpu.memoryUtil*100 <= 10.0) and (gpu.memoryFree/GB >= args.memory_per_gpu):
                gpu_IDs.append(i)
    print(gpu_IDs)


if __name__ == "__main__":
    main()
