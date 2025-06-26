#!/usr/bin/python
import ipaddress
import multiprocessing
import pdb
import subprocess
import os
import psutil
import socket

def pinger( job_q, results_q):
    DEVNULL = open(os.devnull, 'w')
    while True:
        ip = job_q.get()
        if ip is None: break

        print(f"Pinging {ip}")
        try:
#            subprocess.check_call(['ping', '-W20', '-c1', ip], stdout=DEVNULL)
            subprocess.check_call(['ping', '-W2', '-c1', ip], stdout=DEVNULL)
            results_q.put(ip)
        except:
            pass

def main():
    pdb.set_trace()
    local_ip = get_ip_address()
    print(f"My local IP address is: {local_ip}")
    interface, subnet = get_local_network(local_ip)
    print(f"interface: {interface}, subnet: {subnet}")
    network = get_network(local_ip, subnet)
    network_address, cidr = get_network_address_and_cidr(network)
    print(f"{network_address}/{cidr}")
    hosts = scan_network(network)
#    hosts = []
    network_address = '.'.join(str(network_address).split('.')[0:3])
    for h in sorted(hosts):
        print(f"{network_address}.{h}")

def get_local_network(ip_address):
    # Get network interface addresses
    addrs = psutil.net_if_addrs()

    # Loop through interfaces
    for interface_name, interface_addresses in addrs.items():
        for address in interface_addresses:
            if address.family == socket.AF_INET:
                if address.address == ip_address:
                    return interface_name, address.netmask

def get_network(ip_address, subnet_mask):
    network = ipaddress.IPv4Network(f"{ip_address}/{subnet_mask}", strict=False)
    return network

def get_network_address_and_cidr(network):
    network_address = network.network_address
    cidr = network.prefixlen
    
    return network_address, cidr

def get_ip_address():
    # More reliable way to get local IP
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("8.8.8.8", 80))
    local_ip = s.getsockname()[0]
    s.close()
    return local_ip

def get_cidr(subnet_mask):
    network = ipaddress.ip_network(f"0.0.0.0/{subnet_mask}", strict=False)
    cidr = network.prefixlen
    return cidr

def scan_network(network):
    all_addresses = list(network.hosts())
    pool_size = len(all_addresses)
    pool_size = 1
    jobs = multiprocessing.Queue()
    results = multiprocessing.Queue()
    pool = [multiprocessing.Process(target=pinger, args=(jobs, results)) for _ in range(pool_size)]
    for p in pool:
        p.start()
    for ip in network.hosts():
        jobs.put(str(ip))
    for _ in pool:
        jobs.put(None)
    for p in pool:
        p.join()
    hosts = []
    while not results.empty():
        ip = results.get()
        hosts.append(int(ip.split('.')[3]))
    return sorted(hosts)


if __name__ == '__main__':
    main()
