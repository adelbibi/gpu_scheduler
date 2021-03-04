import time
from fabric import Connection


class Scheduler(object):
    def __init__(self):
        # torrnode3 > issues with password
        # torrnode6 > gpus down
        self.allhosts = ['torrnode1', 'torrnode2', 'torrnode4', 'torrnode5', 'torrnode7', 'torrnode8']
        self.gpu_list = {}
        self.hostname = None
        self.gpu_indices = None
        self.num_gpus = None

    def ping_avail_gpus(self):
        '''
            Keeps pining Torrnodes until it returns at least
            one free avialble GPU
        '''
        print('########## Refresh List of GPUs ###########')
        self._get_gpu_list()

        while(len(self.gpu_list) == 0):
            print('No available GPUs found. Refreshing in few seconds!')
            time.sleep(30)
            self._get_gpu_list()

        self.gpu_indices = self.gpu_list[self.hostname]
        self.num_gpus = len(self.gpu_list[self.hostname])

    def _get_gpu_list(self):
        max_number_gpus = 0
        for host in self.allhosts:
            c = Connection(host)
            result = c.run('python gpu_crawler.py --memory_per_gpu 11 --card_exception "Tesla K40m"', hide=True)
            all_IDs = result.stdout.replace('[', '').replace(']','').replace('\n', ''). replace(' ', '')
            all_IDs = all_IDs.split(',')
            if len(all_IDs) == 1 and all_IDs[0] == '':
                continue
            self.gpu_list[host] = all_IDs
            if len(all_IDs) > max_number_gpus:
                max_number_gpus = len(all_IDs)
                self.hostname = host
        for hostname, list_gpu_numbers in self.gpu_list.items():
            for gpu_number in list_gpu_numbers:
                print('Avail GPU: {} #{}.'.format(hostname, gpu_number))

    def launch_job(self, my_command):
        with Connection(self.hostname) as c:
            c.run(my_command, hide=True)
