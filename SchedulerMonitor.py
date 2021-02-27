
from fabric import Connection
import time
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

