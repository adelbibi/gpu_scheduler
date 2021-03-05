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


def main():
    miniSLURM = Scheduler()
    miniSLURM.ping_avail_gpus()
    print('Hostname with largest free GPUs without exception cards: {}'.format(miniSLURM.hostname))
    print('Corresponding GPU Indices on this Node that are free: {}'.format(miniSLURM.gpu_indices))

    # if len(args.task_id) == 1 and args.task_id[0] == -1:
    #     while(completed_jobs < len(task_list)):
    #         my_all_str = ''
    #         for i in range(min(miniSLURM.num_gpus, len(task_list) - completed_jobs)):
    #             if i == 0:
    #                 my_all_str += get_python_command_run(miniSLURM.gpu_indices[i], completed_jobs)
    #             else:
    #                 my_all_str += '&' + get_python_command_run(miniSLURM.gpu_indices[i], completed_jobs)
    #             completed_jobs += 1
    #         final = f'cd geometric_certification ; conda activate geo_rs ;  ' + my_all_str
    #         print('#######################')
    #         print('Running Jobs on Node: {}'.format(miniSLURM.hostname))
    #         print(final)
    #         miniSLURM.launch_job(final)
    #         miniSLURM.ping_avail_gpus()
    # def get_python_command_run(gpu_num, task_id):
    #     my_str_command = ''
    #     my_str_command += f'CUDA_VISIBLE_DEVICES={gpu_num} python train.py ' + get_task(task_id, False)  + ' --experiment-name ' + str(task_id)
    #     return my_str_command


    # def get_task(index, verbose):
    #     task_params = dict(zip(all_params.keys(), task_list[index]))
    #     if verbose:
    #         print(task_params)
    #     return ' '.join(f'--{k} {v}' for k, v in task_params.items())

if __name__ == "__main__":
    main()
