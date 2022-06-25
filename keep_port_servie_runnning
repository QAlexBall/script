#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import time
import socket
import asyncio
import sys
import json

if len(sys.argv) is not 5:
    print("remote_host, remote_user, ssh_port, tunnel_host, port_list")
remote_host = sys.argv[1]
remote_user = sys.argv[2]
ssh_port = sys.argv[3]
tunnel_host = sys.argv[4]
port_list = json.loads(sys.argv[5])


print(sys.argv)
 
def generate_restart_command_dict(remote_host, remote_user, ssh_port, tunnel_host, port_list):
    d = {}
    for port in port_list:
        # port[0] local_port, port[1] remote_port
        d[str(port[0])] = f"ssh -Nf -p {ssh_port} {port[0]}:{tunnel_host}:{port[1]} {remote_user}:{remote_host}"
    return d


RESTART_COMMAND_DICT = generate_restart_command_dict(remote_host, remote_user, ssh_port, tunnel_host, port_list)
print("commands", RESTART_COMMAND_DICT)


def is_port_open(port):
    is_open = False
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    result = sock.connect_ex(('127.0.0.1', int(port)))
    if result == 0:
        is_open = True
        print("Port %d is open" % int(port))
    else:
        print("Port %d is not open" % int(port))
    sock.close()
    return is_open


async def is_ports_open(port_list):
    is_open_dict = {}
    for port in port_list:
        is_open_dict[port] = True if is_port_open(port) else False
    await asyncio.sleep(5)
    return is_open_dict


def restart_port_service(port):
    cmd = RESTART_COMMAND_DICT[port]
    if not is_port_open(port):
        print("===> restart port service:", cmd)
        os.system(cmd)
    print("===> check again: ")
    is_port_open(port)


def restart_ports_service(port_list):
    for port in port_list:
        restart_port_service(str(port[0]))
        print()


def main():
    while True:
        restart_ports_service(port_list)
        time.sleep(3)



if __name__ == "__main__":
    main()
