from device import Device
from router import Router

class Host(Device):
    """
    """

    def __init__(self, router):
        """
        Creates a Host instance with the specified router.
        """

        # TODO: Check router isinstance(router.Router)
        self._router = router

    def router(self):
        """
        Returns the router to which the host is connected.
        """
        return self._router
