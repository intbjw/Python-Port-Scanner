import socket


def scan(host, port):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        s.connect((host, port))
        print("Port open: " + str(port))
        s.close()
    except:
        print("Port closed:" + str(port))


host = "192.168.126.5"
# for port in [21, 22, 80, 135, 8888]:
for port in [135]:
    scan(host, port)
