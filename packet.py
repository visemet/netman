from device import Device

class Packet:
    """
    Builder for Packet instances.
    """

    _ACK = 'ack'

    _DATA_SIZE = 8000
    _ACK_SIZE = 512

    def __init__(self):
        """
        Creates a Packet instance.
        """

        # Initializes attributes as None
        self._id = None
        self._source = None
        self._bits_size = None
        self._dest = None
        self._create_time = None

        # Initializes the packet data
        self._data = {}

    def set_create_time(self, time):
        self._create_time = time
    
    def get_create_time(self):
        return self._create_time
    
    def __repr__(self):
        """
        Defines the string representation for a Packet instance.
        """

        return ('Packet['
                'id=%s, '
                'source=%s, '
                'dest=%s, '
                'data=%s'
                ']') % (self.seq(), self.source(), self.dest(), self._data)

    def seq(self, num=None):
        """
        seq()    -> returns the sequence number

        seq(num) -> sets the sequence number as the specified value
        """

        if num is None:
            return self._id

        # Checks that num is an int
        if not isinstance(num, int):
            raise TypeError, 'num must be an int'

        self._id = num

    def source(self, device=None):
        """
        source()       -> returns the source

        source(device) -> sets the source as the specified value
        """

        if device is None:
            return self._source

        # Checks that device is a Device instance
        if not isinstance(device, Device):
            raise TypeError, 'device must be a Device instance'

        self._source = device

    def dest(self, device=None):
        """
        dest()       -> returns the destination

        dest(device) -> sets the source as the specified value
        """

        if device is None:
            return self._dest

        # Checks that device is a Device instance
        if not isinstance(device, Device):
            raise TypeError, 'device must be a Device instance'

        self._dest = device

    def size(self, bits=None):
        """
        size()     -> returns the packet size

        size(bits) -> sets the packet size as the specified value
        """

        if bits is None:
            return self._bits_size

        # Checks that bits is an int
        if not isinstance(bits, int):
            raise TypeError, 'bits must be an int'

        self._bits_size = bits

    def has_datum(self, key):
        """
        Returns True if the packet contains a datum for the specified
        key, and False otherwise.
        """

        return key in self._data

    def datum(self, key, value=None):
        """
        datum(key)        -> returns the value associated with the
                             specified key

        datum(key, value) -> adds the specified key-value pair
        """

        if value is None:
            return self._data[key]

        self._data[key] = value
