from fabric import Connection

# torrnode3 > issues with password
# torrnode6 > gpus down
hosts = ['torrnode1', 'torrnode2', 'torrnode4', 'torrnode5', 'torrnode7', 'torrnode8']


def main():
    dict_all = {}
    for host in hosts:
        print(host)
        c = Connection(host)
        result = c.run('python gpu_crawler.py --memory_per_gpu 11', hide=True)
        all_IDs = result.stdout.replace('[', '').replace(']','').replace('\n', ''). replace(' ', '')
        all_IDs = all_IDs.split(',')
        dict_all[host] = all_IDs
    print(dict_all)


if __name__ == "__main__":
    main()
