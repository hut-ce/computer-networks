#!/usr/bin/env python
# Python Network Programming Cookbook -- Chapter - 1
# This program is optimized for Python 2.7.
# It may run on any other version with/without modifications.
import socket

def printServiceOnPort(port, protocol):
    try:
        serviceName = socket.getservbyport(port, protocol);
        print(f'Port:  {port}, Service: {serviceName}');
    except:
        pass

if __name__ == '__main__':
    protocols = ['tcp', 'udp']

    for prtcl in protocols:
        for p in range(10, 1023):
            printServiceOnPort(p, prtcl)
