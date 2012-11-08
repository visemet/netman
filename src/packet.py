from device import Device

class Packet:
    """
    Builder for Packet instances.
    """

    def __init__(self):
        """
        Creates a Packet instance.
        """

        self._data = dict()

    def __str__(self):
        """
        """

        return 'Packet[source=%s, destination=%s, data=%s]' % (self.source(), self.destination(), self._data)

    def __repr__(self):
        """
        """

        return self.__str__()

    def has(self, key):
        """
        Returns whether the packet contains data for the specified key.
        """

        return key in self._data

    def datum(self, key, value=None):
        """
        datum(key)        -> returns the value associated with the
                             specified key

        datum(key, value) -> adds the specified key-value pair and
                             returns this instance
        """

        if value is None:
            return self._data[key]

        self._data[key] = value
        return self

    def identifier(self, identifier=None):
        """
        identifier()           -> returns the identifier

        identifier(identifier) -> sets the identifier as the specified
                                  value and returns this instance
        """

        if identifier is None:
            return self._identifier

        # Checks that identifier is an int
        if not isinstance(identifier, int):
            raise TypeError, 'identifier must be an int'

        self._identifier = identifier
        return self

    def source(self, source=None):
        """
        source()       -> returns the source

        source(source) -> sets the source as the specified value and
                          returns this instance
        """

        if source is None:
            return self._source

        # Checks that source is a Device instance
        if not isinstance(source, Device):
            raise TypeError, 'source must be a Device instance'

        self._source = source
        return self

    def destination(self, destination=None):
        """
        destination()            -> returns the destination

        destination(destination) -> sets the source as the specified
                                    value and returns this instance
        """

        if destination is None:
            return self._destination

        # Checks that destination is a Device instance
        if not isinstance(destination, Device):
            raise TypeError, 'destination must be a Device instance'

        self._destination = destination
        return self
