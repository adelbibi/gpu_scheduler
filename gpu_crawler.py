import argparse
import GPUtil as GPU

parser = argparse.ArgumentParser(description='GPU Scheduler')
parser.add_argument("--memory_per_gpu", type=int, default=11, help="specify free per gpu memory requirement in GB")

args = parser.parse_args()


def main():
    GB = 1024
    gpu_IDs = []
    GPUs = GPU.getGPUs()
    for i in range(len(GPUs)):
        gpu = GPUs[i]
        if (gpu.load*100.0 < 20.0) and (gpu.memoryUtil*100 <= 10.0) and (gpu.memoryFree/GB >= args.memory_per_gpu):
            # print("GPU RAM Free: {0:.0f}MB | Used: {1:.0f}MB | Util {2:3.0f}% | Total {3:.0f}MB".format(gpu.memoryFree, gpu.memoryUsed, gpu.memoryUtil*100, gpu.memoryTotal))
            gpu_IDs.append(i)
    print(gpu_IDs)
    # filehandle = open('GPUAvail.txt', 'w')
    # for gpu_num in gpu_IDs:
    #     filehandle.write(str(gpu_num) + '\n')


if __name__ == "__main__":
    main()
