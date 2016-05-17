import re
from ida.signals.trace import IDATrace

class IDAStream(object):

    def __init__(self, traces=None):
        self._traces = []
        if isinstance(traces, IDATrace):
            self._traces = [traces]
        if traces:
            self._traces.extend(traces)


    @property
    def traces(self):
        return self._traces


    @traces.setter
    def traces(self, traces):
        self._traces = traces


    def append(self, trace):
        if not isinstance(trace, IDATrace):
            raise TypeError('trace must be of type IDATrace')

        self.traces.append(trace)


    def select(self, station=None, channel=None, location=None, component=None):

        # A new Stream object is returned but the traces it contains are just aliases to the traces of the original stream.
        # Does not copy the data but only passes a reference.

        # all matching done using regular expressions (module re)

        traces = []
        for trace in self:
            # skip trace if any given criterion is not matched
            if station is not None:
                station = station.upper()
                if not re.fullmatch(station, trace.station):
                    continue

            if location is not None:
                if not re.fullmatch(location, trace.location):
                    continue

            if channel is not None:
                channel = channel.upper()
                if not re.fullmatch(channel, trace.channel):
                    continue

            if component is not None:
                component = component.upper()
                if len(trace.channel) < 3:
                    continue
                if not (trace.channel[-1] == component):
                    continue

            traces.append(trace)

        return self.__class__(traces=traces)


    def has_trace(self, trace):
        if not isinstance(trace, IDATrace):
            raise TypeError('trace must be of type IDATrace')

        return trace in self.traces


    def remove_trace(self, trace):
        if not isinstance(trace, IDATrace):
            raise TypeError('trace must be of type IDATrace')

        self.traces.remove(trace)


    def __len__(self):
        return len(self.traces)

    def __iter__(self):
        return list(self.traces).__iter__()

    def __getitem__(self, index):
        """
        :return: Trace objects
        """
        if isinstance(index, slice):
            return self.__class__(traces=self.traces.__getitem__(index))
        else:
            return self.traces.__getitem__(index)

    def __str__(self, extended=False):
        """
        Return short summary string of the current stream.

        It will contain the number of Traces in the Stream and the return value
        of each Trace's :meth:`~Trace.__str__` method.

        :type extended: bool, optional
        :param extended: This method will show only 20 traces by default.
            Enable this option to show all entries.

        """

        # get longest id
        if self.traces:
            id_length = self and max(len(tr.id) for tr in self) or 0
        else:
            id_length = 0
        out = str(len(self.traces)) + ' Trace(s) in Stream:\n'
        if len(self.traces) <= 20 or extended is True:
            out = out + "\n".join([_i.__str__(id_length) for _i in self])
        else:
            out = out + "\n" + self.traces[0].__str__() + "\n" + \
                '...\n(%i other traces)\n...\n' % (len(self.traces) - 2) + \
                self.traces[-1].__str__() + '\n\n[Use "print(' + \
                'Stream.__str__(extended=True))" to print all Traces]'
        return out

