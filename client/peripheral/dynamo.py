"""
    Dynamo
"""

import threading

DYNAMO_TYPE = {
    'NOTSET': 0,
    'BIKE': 1,
    'TREADMILL': 2
}

class Dynamo:
    """
        Dynamo class
    """
    def __init__(self, **kwargs):
        """
        kwargs:
            bt_address: Bluetooth address of the device
            uuid: UUID of the device
            type: machine type (BIKE, TREADMILL), default to NOTSET
        """
        self.mutex = threading.Lock()
        self.bt_address = kwargs.get('bt_address', None)
        self.uuid = kwargs.get('uuid', None)
        self.session_id = None
        self.type = DYNAMO_TYPE[kwargs.get('type', 'NOTSET')]
        self.t_prod = set()

    def prod_sum(self) -> float:
        """
            Return the sum of the accumulated production (in Watt)
        """
        self.mutex.acquire(blocking=True)
        mem = sum(self.t_prod)
        self.t_prod.clear()
        self.mutex.release()
        return mem

    def add_prod(self, prod: float) -> None:
        """
            Add a production value (in Watt) to the set
            arg:
                prod: production value in Watt
        """
        self.mutex.acquire(blocking=True)
        self.t_prod.add(prod)
        self.mutex.release()

    def query_type(self) -> bool:
        ## if self.bt_address:
            ## BT COM
            ## if com fails:
            ##   return false
            ## self.type = ...
            ## pass
        return True
