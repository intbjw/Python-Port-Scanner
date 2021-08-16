#!/usr/bin/python
# 1.采用SYN扫描更加的隐蔽
# 2.使用scapy进行网络发包
# 3.
from scapy.all import *
from pyfiglet import Figlet
import argparse
logo = Figlet(font='graffiti')
print(logo.renderText('PortScanner'))


def _argparse():
    parser = argparse.ArgumentParser(description="Python SYN 端口扫描")
    parser.add_argument('-t', '--target', action='store', dest='host', help="目标主机IP ")
    if len(sys.argv) == 1:
        parser.print_help()
        sys.exit()
    return parser.parse_args()


def checkhost(ip):
    ping = IP(dst=ip)/ICMP()
    res = sr1(ping, timeout=1, verbose=0)
    if res == None:
        print("This host is down")
    else:
        print("This host is up")


# function to check open port
def checkport(ip, port):
    tcp_request = IP(dst=ip)/TCP(dport=port, flags="S")
    tcp_response = sr1(tcp_request, timeout=1, verbose=0)
    try:
        if tcp_response.getlayer(TCP).flags == "SA":
            print(port, "is listening")
    except AttributeError:
        print(port, "is not listening")


def main():
    parser = _argparse()
    ip = parser.host
    checkhost(ip)
    port = 82
    checkport(ip, port)


if __name__ == '__main__':
    main()
