import socket
import pickle
import sys
import _thread
import threading

import rtt


class RUDPDatagram:
    timestamp: float
    sequence_no: int
    payload: bytes

    def __init__(self, **kwargs):
        self.payload = kwargs["payload"]
        self.address = kwargs["address"]
        self.sequence_no = kwargs["sequence_no"]
        self.timestamp = kwargs["timestamp"]


class RUDPServer:
    def __init__(self, port: int):
        try:
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            self.socket.bind(("0.0.0.0", port))
        except:
            print("Couldn't initialise server", file=sys.stderr)
            sys.exit(1)

    def receive(self):
        message, address = self.socket.recvfrom(1024)
        datagram = pickle.loads(message)

        self.last_seqno = datagram.sequence_no
        self.last_ts = datagram.timestamp

        return (datagram.payload, address)

    def reply(self, address, payload: bytes):
        datagram = RUDPDatagram(payload=payload, address=address,
                                sequence_no=self.last_seqno, timestamp=self.last_ts)
        serialised_datagram = pickle.dumps(datagram)

        self.socket.sendto(serialised_datagram, address)


class RUDPClient:
    def __init__(self, hostname: str, port: int):
        self.__hostname = hostname
        self.__port = port
        self.__sequence_no = 0
        self.__rtt = rtt.RTT()

        try:
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            self.socket.setblocking(False)
        except:
            print("Couldn't initialise client", file=sys.stderr)
            sys.exit(1)

    def send_recv(self, payload: bytes):
        timestamp = self.__rtt.timestamp()
        datagram = RUDPDatagram(
            address=(self.__hostname, self.__port),
            payload=payload, sequence_no=self.__sequence_no, timestamp=timestamp)
        serialised_datagram = pickle.dumps(datagram)

        self.__rtt.new_packet()

        # Si conocen una mejor forma menos cursed de hacer esto, háganmelo
        # saber, porfa. Lo estoy haciendo así porque la implementación original
        # en C usa goto y acá no podemos hacer eso

        # Lección de todo esto: no crean que *siempre* está mal usar goto. Hay
        # veces en que es más práctico usarlos, lo que no quita que hay que
        # usarlos bien. De hecho, si revisan el código fuente de Linux, verán
        # que en ocasiones usan goto. Si Linus Torvalds considera que está bien
        # usarlos (él revisa todos los commits y si encuentra algo que no le
        # gusta... digamos que se pone Paty Cofré con la persona que lo hizo)

        event = threading.Event()

        def timeout():
            print("timeout")
            if self.__rtt.timeout():
                _thread.interrupt_main()
            else:
                event.set()

        response = None
        attempting_send = True
        while attempting_send:
            event.clear()
            self.socket.sendto(serialised_datagram,
                               (self.__hostname, self.__port))

            timer = threading.Timer(self.__rtt.start(), timeout)
            timer.start()

            datagram = None
            while True:
                try:
                    if event.wait(timeout=0.05):
                        break

                    message = self.socket.recv(1024)
                    response = pickle.loads(message)
                except BlockingIOError:
                    continue

                if response.sequence_no == self.__sequence_no:
                    attempting_send = False
                    break

        timer.cancel()
        self.__rtt.stop(self.__rtt.timestamp() - response.timestamp)

        return response.payload
