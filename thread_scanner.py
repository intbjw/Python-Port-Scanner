#!/usr/bin/python3
# -*- coding:utf-8 -*-


import socket
import threading
import sys
import argparse
import queue
import time
import random


# 端口扫描类，继承threading.Thread
class PortScanner(threading.Thread):
    # 需要传入端口队列、目标IP、探测超时时间
    def __init__(self, portqueue, ip, timeout=3):
        threading.Thread.__init__(self)
        self._portqueue = portqueue
        self._ip = ip
        self._timeout = timeout

    def run(self):
        while True:
            # 判断端口队列是否为空
            if self._portqueue.empty():
                # 端口队列为空，说明扫描完毕，跳出循环
                break
            # 从端口队列中取出端口，超时时间为1S
            port = self._portqueue.get(timeout=0.5)
            try:
                s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                s.settimeout(self._timeout)
                result_code = s.connect_ex((self._ip, port))
                # 若端口开放，则会
                if result_code == 0:
                    sys.stdout.write("[%d] OPEN\n" % port)
            except Exception as e:
                print(e)
            finally:
                s.close()


def StartScan(targetip, port, threadNum):
    # 端口列表
    portList = []
    # 判断是单个端口还是范围端口
    if '-' in port:
        for i in range(int(port.split('-')[0]), int(port.split('-')[1])+1):
            portList.append(i)
    else:
        portList.append(int(port))
    # 目标IP地址
    ip = targetip
    # 线程列表
    # 增加随机重排扫描算法，从而使"基于通过连续端口被连接算法进行扫描判断"的方式失效
    random.shuffle(portList)
    threads = []
    threadNumber = threadNum
    # 端口队列
    portQueue = queue.Queue()
    # 生成端口，加入端口队列
    for port in portList:
        portQueue.put(port)
    for t in range(threadNumber):
        threads.append(PortScanner(portQueue, ip, timeout=3))
    # 启动线程
    for thread in threads:
        time.sleep(0.01)
        thread.start()
    # 阻塞线程
    for thread in threads:
        thread.join()


def _argparse():
    parser = argparse.ArgumentParser(description="Python端口扫描 多线程")
    parser.add_argument('-i', '--ip', action='store', dest='ip', help="目标主机IP ")
    parser.add_argument('-p', '--port', action='store', dest='port', help='端口 支持单个端口或1-100')
    parser.add_argument('-t', '--thread', action='store', dest='threadNum', default=100, help='扫描进程数')
    if len(sys.argv) == 1:
        parser.print_help()
        sys.exit()
    return parser.parse_args()


if __name__ == '__main__':
    parser = _argparse()
    start = time.time()
    StartScan(parser.ip, parser.port, parser.threadNum)
    end = time.time()
    print(f'用时：{end-start}')






