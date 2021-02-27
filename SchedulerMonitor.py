
from fabric import Connection

# torrnode3 > issues with password
# torrnode6 > gpus down


class Scheduler(object):
    def __init__(self):
        self.allhosts = ['torrnode1', 'torrnode2', 'torrnode4', 'torrnode5', 'torrnode7', 'torrnode8']
        self.hostname = None
        self.gpu_indices = None
        self.num_gpus = None
        self.username = None

    def get_my_jobs(self, my_username):
        '''
        get all my running gpus > need to have a tail function code on cluster and parse name
        '''
        self.username = my_username
        pass

    def ping_avail_gpus(self):
        '''
            Keeps pining Torrnodes until it returns at least
            one free avialble GPU
        '''
        gpu_list, hostname_choice = self._get_gpu_list()
        while(len(gpu_list) == 0):
            print('########## Refresh List of GPUs ###########')
            time.sleep(60)
            gpu_list, hostname_choice = self._get_gpu_list()

        self.hostname = hostname_choice
        self.gpu_indices = gpu_list[hostname_choice]
        self.num_gpus = len(gpu_list[hostname_choice])

    def _get_gpu_list(self):
        gpu_list = {}
        max_number_gpus = 0
        for host in self.allhosts:
            c = Connection(host)
            result = c.run('python gpu_crawler.py --memory_per_gpu 11', hide=True)
            all_IDs = result.stdout.replace('[', '').replace(']','').replace('\n', ''). replace(' ', '')
            all_IDs = all_IDs.split(',')
            if len(all_IDs) == 1 and all_IDs[0] == '':
                continue
            gpu_list[host] = all_IDs
            if len(all_IDs) > max_number_gpus:
                max_number_gpus = len(all_IDs)
                hostname_choice = host
        # print('Number of available GPS: {}'.format(len(gpu_list)))
        for hostname, avil_gpu in gpu_list.items():
            for gpu_number in avil_gpu:
                print('Avail GPU: {} #{}.'.format(hostname, gpu_number))
        return gpu_list, hostname_choice

    def launch_job(self, my_command):
        c = Connection(self.hostname)
        c.run(my_command, hide=True)



def main():
    miniSLURM = Scheduler()
    miniSLURM.ping_avail_gpus()
    
    
    
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

