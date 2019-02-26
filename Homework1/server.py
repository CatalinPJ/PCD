import socket
import time

class ServerTCPStream:
    def __init__(self):
        pass
    def doWork(self):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.bind((socket.gethostname(), 8756))
        s.listen(1)
        print("Listening...")
        while True:
            (conn, address) = s.accept()
            text_file = 'file'
            _time_start = time.time()
            with open(text_file, "wb") as fw:
                print("Receiving..")
                while True:
                    # print('receiving')
                    data = conn.recv(1024)
                    # print('Received: ', data)
                    if not data:
                        print('Breaking from file write')
                        break
                    fw.write(data)
                fw.close()
                _time_finish = time.time()
                print("Received..", _time_finish - _time_start)
                conn.close()


class ServerTCPStopAndWait:
    def __init__(self):
        pass
    def doWork(self):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.bind((socket.gethostname(), 8756))
        s.listen(1)
        print("Listening...")
        while True:
            (conn, address) = s.accept()
            text_file = 'file'
            _time_start = time.time()
            with open(text_file, "wb") as fw:
                print("Receiving..")
                while True:
                    data = conn.recv(1024)
                    conn.send(b"ACK")
                    if not data:
                        print('Breaking from file write')
                        break
                    fw.write(data)
                fw.close()
                _time_finish = time.time()
                print("Received..", _time_finish - _time_start)
                conn.close()


class ServerUDPStream:
    def __init__(self):
        pass
    def doWork(self):
        host = "0.0.0.0"
        port = 9999
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.bind((host, port))
        addr = (host, port)
        print("Listening ...")
        _time_start = time.time()
        with open('file', "wb") as fw:
            try:
                while True:
                     data, addr = s.recvfrom(1024)
                     if not data:
                         print('Breaking from file write')
                         break
                     fw.write(data)

            except:
                fw.close()
                s.close()
                time_finish = time.time()
                print("Received..", time_finish - _time_start)


class ServerUDPStopAndWait:
    def __init__(self):
        pass
    def doWork(self):
        host = "0.0.0.0"
        port = 9999
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.bind((host, port))
        print("Listening ...")
        _time_start = time.time()
        with open('file', "wb") as fw:
            try:
                while True:
                     data, addr = s.recvfrom(1024)
                     s.sendto(b'ACK', addr)
                     if not data:
                         print('Breaking from file write')
                         break
                     fw.write(data)

            except:
                fw.close()
                s.close()
                time_finish = time.time()
                print("Received..", time_finish - _time_start)


class ServerFactory:
    def __init__(self):
        pass
    def getServer(self, protocol, mechanism):
        if protocol == 'TCP' and mechanism == 'STREAM':
            return ServerTCPStream()
        elif protocol == "UDP" and mechanism == "STREAM":
            return ServerUDPStream()
        elif protocol == "TCP" and mechanism == "SW":
            return ServerTCPStopAndWait()
        elif protocol == "UDP" and mechanism == "SW":
            return ServerUDPStopAndWait()
        else:
            return None


if __name__ == "__main__":
    protocol = "UDP"
    mechanism = "SW"
    server = ServerFactory().getServer(protocol, mechanism)
    if server:
        server.doWork()