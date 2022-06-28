import datetime

RTT_RXTMIN = 0.5
RTT_RXTMAX = 60
RTT_MAXNREXMT = 5


class RTT:
    def __rtt_minmax(self, rto: float):
        if rto < RTT_RXTMIN:
            rto = RTT_RXTMIN
        elif rto > RTT_RXTMAX:
            rto = RTT_RXTMAX

        return rto

    def __rtt_rtocalc(self):
        return self.__srtt + (4.0 * self.__rttvar)

    def __init__(self):
        self.__base = datetime.datetime.now().timestamp()

        self.__rtt = 0.0
        self.__srtt = 0.0
        self.__rttvar = 0.75
        self.__rto = self.__rtt_minmax(self.__rtt_rtocalc())

    def timestamp(self):
        epoch = datetime.datetime.now().timestamp()

        return epoch - self.__base

    def new_packet(self):
        self.__nrexmt = 0

    def start(self):
        return self.__rto + 0.5

    def stop(self, ms: int):
        self.__rtt = ms / 1000.0

        delta = self.__rtt - self.__srtt
        self.__srtt += delta / 8.0

        delta = abs(delta)

        self.__rttvar += (delta - self.__rttvar) / 4
        self.__rto = self.__rtt_minmax(self.__rtt_rtocalc())

    def timeout(self):
        self.__rto *= 2

        self.__nrexmt += 1
        if self.__nrexmt > RTT_MAXNREXMT:
            return True

        return False
