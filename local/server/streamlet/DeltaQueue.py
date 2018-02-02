
"""
Provides DeltaQueue, a data structure for storing a bunch of deltas.
Whenever possible, deltas are combined.
"""

from streamlet import data_frame_proto

class DeltaQueue:
    """Accumulates a bunch of deltas."""

    def __init__(self):
        """Constructor."""
        self._empty()

    def add_delta(self, delta):
        """Accumulates this delta into the list."""
        # Store the index if necessary.
        if (delta.id in self._id_map):
            index = self._id_map[delta.id]
        else:
            index = len(self._deltas)
            self._id_map[delta.id] = index
            self._deltas.append(None)

        # Combine the previous and new delta.
        self._deltas[index] = self.compose(self._deltas[index], delta)

    def get_deltas(self):
        """Returns a list of deltas in a DeltaList message
        and clears this queue."""
        deltas = self._deltas
        self._empty()

        return deltas

    def _empty(self):
        """Returns this Accumulator to an empty state."""
        self._deltas = []
        self._id_map = {}

    @staticmethod
    def compose(delta1, delta2):
        """Combines the two given deltas into one."""
        if delta1 == None:
            return delta2
        elif delta2.WhichOneof('type') == 'new_element':
            return delta2
        elif delta2.WhichOneof('type') == 'add_rows':
            data_frame_proto.add_rows(delta1, delta2)
            return delta1

        print('delta1')
        print(delta1)
        print('delta2')
        print(delta2)
        raise NotImplementedError('Need to implement the compose code.')