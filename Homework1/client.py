import socket


file_name = "file"


def create_file(size):
    f = open(file_name, "wb")
    f.seek(size*1024)
    f.write(b"\0")
    f.close()


class ClientTCPStream:
    def __init__(self):
        pass
    def doWork(self, size):
        create_file(size)
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((socket.gethostname(), 8756))

        with open(file_name, 'rb') as fs:
            while True:
                data = fs.read(1024)
                # print('Sending data')
                s.send(data)
                # print('Sent data')
                if not data:
                    print('Breaking from sending data')
                    break
            fs.close()

        s.close()


class ClientTCPStopAndWait:
    def __init__(self):
        pass
    def doWork(self, size):
        create_file(size)
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((socket.gethostname(), 8756))

        with open(file_name, 'rb') as fs:
            while True:
                data = fs.read(1024)
                # print('Sending data')
                s.send(data)

                # print('Sent data')
                if not data:
                    print('Breaking from sending data')
                    break
                d = s.recv(3)
                print(d.decode())
            fs.close()

        s.close()


class ClientUDPStream:
    def __init__(self):
        pass
    def doWork(self, size):
        create_file(size)
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        host = socket.gethostname()
        port = 9999
        addr = (host, port)

        # s.sendto(file_name, addr)

        f = open(file_name, "rb")
        data = f.read(1024)
        while True:
            if (s.sendto(data, addr)):
                # print("sending ...")
                data = f.read(1024)
                if not data:
                    print('Breaking from sending data')
                    break
        f.close()
        s.close()


class ClientUDPStopAndWait:
    def __init__(self):
        pass
    def doWork(self, size):
        create_file(size)
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        host = socket.gethostname()
        port = 9999
        addr = (host, port)

        # s.sendto(file_name, addr)

        f = open(file_name, "rb")
        data = f.read(1024)
        while True:
            if (s.sendto(data, addr)):
                # print("sending ...")
                data = f.read(1024)
                if not data:
                    print('Breaking from sending data')
                    break
                ack, server = s.recvfrom(3)
                print(ack.decode())
        f.close()
        s.close()


class ClientFactory:
    def __init__(self):
        pass
    def getClient(self, protocol, mechanism):
        if protocol == 'TCP' and mechanism == 'STREAM':
            return ClientTCPStream()
        elif protocol == "UDP" and mechanisn == "STREAM":
            return ClientUDPStream()
        elif protocol == "TCP" and mechanisn == "SW":
            return ClientTCPStopAndWait()
        elif protocol == "UDP" and mechanisn == "SW":
            return ClientUDPStopAndWait()
        else:
            return None;


if __name__ == "__main__":
    protocol = "UDP"
    mechanisn = "SW"
    size = 6345
    client = ClientFactory().getClient(protocol, mechanisn)
    if client:
        client.doWork(size)