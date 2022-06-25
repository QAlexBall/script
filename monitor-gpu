import sys
import argparse
import subprocess
import logging
from logging import debug
from functools import partial

parser = argparse.ArgumentParser(description='Check state of GPUs')
parser.add_argument('--ssh-timeout', default=3)
parser.add_argument('--cmd-timeout', default=10)
parser.add_argument('hosts', nargs='*', default=[])


def log_func_name(func):
    def wrapper(*args, **kwargs):
        print("*** Start", func.__name__)
        func(*args, **kwargs)
        print("*** End", func.__name__)
    return wrapper

def run_command(cmd):
    debug('Running command: "{}"'.format(cmd))

    try:
        res = subprocess.check_output(cmd, shell=True)
        return res
    except subprocess.TimeoutExpired as e:
        debug(e.stderr)
    except subprocess.CalledProcessError as e:
        debug(e.stderr)
    return None

def format_connect(cmd, host):
    cmd = cmd.format(host=host.get('host'),
                     port=host.get('port') if host.get('port') is not None else "22",
                     password=host.get('password'))
    return cmd

def check_ssh(cmd, host):
    print("Connect to", host.get('host'))
    hostname = host.get('host').split('@')[0]
    result = {}
    cmd = format_connect(cmd, host)
    res = run_command(cmd)
    res = res.decode('ascii').split('\n')[0] if res is not None else "down"
    result[hostname + "-ssh"] = res
    return result

def check_gpu(cmd, host):
    result = {}
    cmd = format_connect(cmd, host)
    res = run_command(cmd)
    res = res.decode('ascii') if res is not None else 'connect failed'
    res = res.split('\n')
    for gpu in res:
        if gpu != '':
            result["gpu" + gpu] = "up"
    return result

def main(argv):

    SSH_CMD = ('sshpass -p {password} ssh -o "ConnectTimeout=3" {host} -p {port} ' 'echo "up"')
    CHECK_GPU = ('sshpass -p {password} ssh -o "ConnectTimeout=3" {host} -p {port} '
                 "nvidia-smi | grep 'GeForce' | awk '{{print $2}}'")

    GPU_CHECK = ("nvidia-smi")
    REMOTE_GPU_CMD = '{} {}'.format(SSH_CMD, GPU_CHECK)

    args = parser.parse_args(argv)
    hosts = args.hosts
    for host in hosts:
        hostname = host.get('host').split('@')[0]
        result = {}
        check_ssh_result = {'ssh': 'down'}
        check_gpu_result = {}

        check_ssh_cmd= partial(check_ssh, cmd=SSH_CMD, host=host)
        check_gpu_cmd = partial(check_gpu, cmd=CHECK_GPU, host=host)
        check_ssh_result = check_ssh_cmd()
        # if can't connect to host, won't exec check_gpu_cmd
        if check_ssh_result.get(hostname + '-ssh') == 'up':
            check_gpu_result = check_gpu_cmd()
        result = dict(check_ssh_result, **check_gpu_result)
        print(result)

if __name__ == '__main__':
    #  logging.basicConfig(level=logging.DEBUG)
    main(sys.argv[1:])
