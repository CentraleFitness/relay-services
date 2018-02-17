"""
    Dynamo
"""

import threading

class Dynamo:
    """
        Dynamo class
    """
    def __init__(self, address, uuid, **kwargs):
        self.mutex = threading.Lock()
        self.address = address
        self.uuid = uuid
        self.session_id = None
        self.t_prod = set()
        return super().__init__(**kwargs)

    def prod_sum(self) -> float:
        """
            Return the sum of the accumulated production (in Watt)
        """
        self.mutex.acquire(blocking=True)
        mem =  sum(self.t_prod)
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
