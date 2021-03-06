import time
from fabric import Connection


class Scheduler(object):
    def __init__(self):
        # torrnode3 > issues with password
        # torrnode6 > gpus down
        self.allhosts = ['torrnode1', 'torrnode2', 'torrnode4', 'torrnode5', 'torrnode7', 'torrnode8']

    def ping_avail_gpus(self):
        '''
            Keeps pining Torrnodes until it returns at least
            one free avialble GPU with a full list stat
        '''
        print('########## Refresh List of GPUs ###########')
        gpu_list = self._get_gpu_list()
        while(len(gpu_list) == 0):
            print('No available GPUs found. Refreshing in few seconds!')
            time.sleep(30)
            gpu_list = self._get_gpu_list()
        for hostname, list_gpu_numbers in gpu_list.items():
            for gpu_number in list_gpu_numbers:
                print('Avail GPU: {} #{}.'.format(hostname, gpu_number))

    def _get_gpu_list(self):
        gpu_list = {}
        for host in self.allhosts:
            c = Connection(host)
            result = c.run('python gpu_crawler.py --memory_per_gpu 11 --card_exception "Tesla K40m"', hide=True)
            all_IDs = result.stdout.replace('[', '').replace(']','').replace('\n', ''). replace(' ', '')
            all_IDs = all_IDs.split(',')
            if len(all_IDs) == 1 and all_IDs[0] == '':
                continue
            gpu_list[host] = all_IDs
        return gpu_list

    def _is_empty_list(self, all_IDS):
        if len(all_IDS) == 1 and all_IDS[0] == '':
            return -1
        else:
            return all_IDS[0]

    def get_one_gpu(self):
        gpu_ID = -1
        while (gpu_ID == -1):
            print('Searching for a single free GPU!')
            for host in self.allhosts:
                c = Connection(host)
                result = c.run('python gpu_crawler.py --memory_per_gpu 11 --card_exception "Tesla K40m"', hide=True)
                all_IDs = result.stdout.replace('[', '').replace(']','').replace('\n', ''). replace(' ', '')
                all_IDs = all_IDs.split(',')
                gpu_ID = self._is_empty_list(all_IDs)
                if gpu_ID != -1:
                    print(f'Found a GPU on {host} with ID#: {gpu_ID}')
                    break
        return host, gpu_ID

    def launch_single_job(self, hostname, my_command):
        with Connection(hostname) as c:
            c.run(my_command, hide=True, pty=False)

    def launch_job_batch(self, list_commands, dir_path, env_name):
        '''
        Function takes the remote directory path and conda envirnoment name along with a list of commands in the 
        form 'python test.py --arg param'
        '''
        completed_jobs = 0
        while(completed_jobs < len(list_commands)):
            # get one free GPU
            time.sleep(60)
            host, gpu_ID = self.get_one_gpu()
            all_str = list_commands[completed_jobs]
            final = f'cd {dir_path} ; conda activate {env_name} ;  CUDA_VISIBLE_DEVICES={gpu_ID} nohup ' + all_str + f' > logs/my_out{completed_jobs}.out 2>&1  &'
            print('Running Jobs on Node: {}'.format(host))
            print(final)
            self.launch_single_job(host, final)
            completed_jobs += 1


def main():
    miniSLURM = Scheduler()
    miniSLURM.ping_avail_gpus()
    # my_str = ['python test.py --arg param1', 'python test.py --arg param2']
    # dir_path = 'path in remote home torrnode dir'
    # env_name = 'conda environment name'
    # miniSLURM.launch_job_batch(my_str, dir_path, env_name)

if __name__ == "__main__":
    main()
