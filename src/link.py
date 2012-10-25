from device import Device

class Link:
    """
    Builder for Link instances.
    """

    def delay(self, delay=None):
        """
        delay()      -> returns the delay

        delay(delay) -> sets the delay as the specified value and
                        returns this instance
        """

        if delay is None:
            return self._delay

        # TODO: Check delay isinstance(float)
        self._delay = delay
        return self

    def rate(self, rate=None):
        """
        rate()     -> returns the rate

        rate(rate) -> sets the rate as the specified value and returns
                      this instance
        """

        if rate is None:
            return self._rate

        # TODO: Check delay isinstance(float)
        self._rate = rate
        return self

    def source(self, source=None):
        """
        source()       -> returns the source

        source(source) -> sets the source as the specified value and
                          returns this instance
        """

        if source is None:
            return self._source

        # TODO: Check source isinstance(device.Device)
        self._source = source
        return self

    def destination(self, destination=None):
        """
        destination()            -> returns the destination

        destination(destination) -> sets the destination as the
                                    specified value and returns this
                                    instance
        """

        if destination is None:
            return self._destination

        # TODO: Check destination isinstance(device.Device)
        self._destination = destination
        return self
