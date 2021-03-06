import argparse
import GPUtil as GPU

parser = argparse.ArgumentParser(description='GPU Scheduler')
parser.add_argument("--memory_per_gpu", type=int, default=11, help="specify free per gpu memory requirement in GB")
parser.add_argument("--card_exception", nargs='+', type=str, default=[''], help="specify names to exclude")

args = parser.parse_args()


def main():
    GB = 1024
    gpu_IDs = []
    GPU_loads = {}
    GPU_memoryUtil = {}

    # compute avrg stats over 5 runs
    GPUs = GPU.getGPUs()
    for i in range(len(GPUs)):
        GPU_loads[i] = 0
        GPU_memoryUtil[i] = 0
        for j in range(5):
            GPUs_refresh = GPU.getGPUs()
            GPU_loads[i] += GPUs_refresh[i].load
            GPU_memoryUtil[i] += GPUs_refresh[i].memoryUtil
        GPU_loads[i] = GPU_loads[i]/5 * 100.0
        GPU_memoryUtil[i] = GPU_memoryUtil[i]/5 * 100.0

    GPUs = GPU.getGPUs()
    for i in range(len(GPUs)):
        gpu = GPUs[i]
        if gpu.name not in args.card_exception:
            if (GPU_loads[i] < 10.0) and (GPU_memoryUtil[i] <= 10.0) and (gpu.memoryFree/GB >= args.memory_per_gpu):
                gpu_IDs.append(i)
    print(gpu_IDs)


if __name__ == "__main__":
    main()
