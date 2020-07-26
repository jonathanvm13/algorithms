#!/usr/bin/env python
import os
import sys
from io import BytesIO, IOBase


def possible_trips_analysis(possible_trips, incoming, outgoing, start_index, inc_factor):
    """
    Analyze possible trips. Iterate over the possible_trips list using the incremental factor.
    it might be 1(right side) or -1 (left side). Validate both outgoing and incoming rules are met, otherwise
    the trip to the country and the following ones is not possible.
    :param possible_trips: List, original possible trips list. Ie, ['Y', 'N']
    :param incoming: List, incoming rules. Ie, ['N','Y', 'Y']
    :param outgoing:  List, outgoing rules. Ie, ['Y','Y','N']
    :param start_index: Int, start point where the possible_trips list will be iterated. Ie, 0
    :param inc_factor: Int, incremental factor. Ie, 1
    """

    possible_trips_size = len(possible_trips)
    current_index  = int(start_index)

    while possible_trips_size > (current_index + inc_factor) >= 0:
        next_index = current_index + inc_factor
        if not (outgoing[current_index] == 'Y' and incoming[next_index] == 'Y'):
            break

        possible_trips[next_index] = 'Y'
        current_index = next_index


def main():
    airlines = int(input())

    for i in range(airlines):
        number_countries = int(input())

        incoming = list(input())
        outgoing = list(input())

        possible_trips_default = "N" * number_countries

        sys.stdout.write(str("Case #{0}: \n".format(i + 1)))

        for country_index in range(number_countries):
            possible_trips = list(possible_trips_default)
            possible_trips[country_index] = 'Y'

            if outgoing[country_index] != 'N':

                # Iterate over the right side
                possible_trips_analysis(possible_trips, incoming, outgoing, country_index, 1)

                # Iterate over the left side
                possible_trips_analysis(possible_trips, incoming, outgoing, country_index, -1)

            sys.stdout.write(str("".join(possible_trips) + '\n'))


# region fastio

BUFSIZE = 8192


class FastIO(IOBase):
    newlines = 0

    def __init__(self, file):
        self._fd = file.fileno()
        self.buffer = BytesIO()
        self.writable = "x" in file.mode or "r" not in file.mode
        self.write = self.buffer.write if self.writable else None

    def read(self):
        while True:
            b = os.read(self._fd, max(os.fstat(self._fd).st_size, BUFSIZE))
            if not b:
                break
            ptr = self.buffer.tell()
            self.buffer.seek(0, 2), self.buffer.write(b), self.buffer.seek(ptr)
        self.newlines = 0
        return self.buffer.read()

    def readline(self):
        while self.newlines == 0:
            b = os.read(self._fd, max(os.fstat(self._fd).st_size, BUFSIZE))
            self.newlines = b.count(b"\n") + (not b)
            ptr = self.buffer.tell()
            self.buffer.seek(0, 2), self.buffer.write(b), self.buffer.seek(ptr)
        self.newlines -= 1
        return self.buffer.readline()

    def flush(self):
        if self.writable:
            os.write(self._fd, self.buffer.getvalue())
            self.buffer.truncate(0), self.buffer.seek(0)


class IOWrapper(IOBase):
    def __init__(self, file):
        self.buffer = FastIO(file)
        self.flush = self.buffer.flush
        self.writable = self.buffer.writable
        self.write = lambda s: self.buffer.write(s.encode("ascii"))
        self.read = lambda: self.buffer.read().decode("ascii")
        self.readline = lambda: self.buffer.readline().decode("ascii")


sys.stdin, sys.stdout = IOWrapper(sys.stdin), IOWrapper(sys.stdout)
input = lambda: sys.stdin.readline().rstrip("\r\n")

# endregion

if __name__ == "__main__":
    main()
