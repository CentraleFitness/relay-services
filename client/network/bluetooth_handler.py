"""
    Bluetooth Handler
    Status: In progress (Not implemented)
"""


class BluetoothHandler:
    """
    Represent the connection between to hotspot and one of the dynamo
    """
    def __init__(self, **kwargs):
        """
        Class contructor
        args:
            None
        kwargs:
            None
        """
        self.address = 0x01
        self.name = "BT Server"
        self.mode = "Central"
        self.type = "Server"
        self.clients = {}
        return super().__init__(**kwargs)
