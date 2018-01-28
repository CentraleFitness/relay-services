import sys
import requests
import random
import argparse

from config.master import *

class Dynamo:
    def __init__(self, address, uuid, **kwargs):
        self.address = address
        self.uuid = uuid
        self.session_id = None
        self.t_prod = list()
        return super().__init__(**kwargs)

    def prod_sum(self) -> float:
        mem =  sum(self.t_prod)
        self.t_prod.clear()
        return mem


class BluetoothHandler:
    def __init__(self, **kwargs):
        self.address = 0x01
        self.name = "BT Server"
        self.mode = "Central"
        self.type = "Server"
        self.clients = {}
        return super().__init__(**kwargs)


class ClientHandler:
    def __init__(self, api_key):
        self.url = SERVER_URL
        self.api_key = api_key
        self.timeout = 1

    def get_module_id(self, mlists: list) -> dict:
        try:
            resp = requests.post(
                self.url,
                json=
                {
                    'api_key': self.api_key,
                    'uuid': mlists
                },
                timeout=self.timeout)
            resp.raise_for_status()
        except Exception:
            print("Something happened")
            return None
        jresp = resp.json()
        if jresp["status"] == "ko":
            ## Handle that error
            print(jresp["reason"])
            return None
        if isinstance(jresp["id"], dict):
            return jresp["id"]

    def module_send_production(self, prod_d: dict):
        return None


def random_range(floor: float, ceil: float, point: int) -> float:
    return round(random.uniform(floor, ceil), point)
        
if __name__ == "__main__":
    random.seed()
    parser = argparse.ArgumentParser(description="API communication experiment")
    parser.add_argument('--range',
                        help="Production range (in Watt)",
                        nargs=2,
                        metavar=('min', 'max'),
                        type=float,
                        action='store',
                        default=(1, 5))
    parser.add_argument('--point',
                        help="Number of digits after the floating point",
                        type=int,
                        action='store',
                        default=2)
    args = parser.parse_args()
    client = ClientHandler("0001-2083-a4b2-c00f")
    modules = [
        Dynamo(address, uuid) for address, uuid in
        ((0x2, "001:001:001"), (0x3, "001:001:002"))
        ]

    print("POST /getModuleId")
    id_dict = client.get_module_id((dynamo.uuid for dynamo in modules))
    for dynamo in modules:
        if dynamo.uuid in id_dict:
            dynamo.session_id = id_dict[dynamo.uuid]
            print("uuid: {}, session_id {}".format(dynamo.uuid,
                                                   dynamo.session_id))
        else:
            print("missing session_id for module {}".format(dynamo.uuid))

    execution = True
    prod_d = dict()
    while execution:
        prod_d.clear()
        for dynamo in modules:
            dynamo.t_prod.append(
                random_range(args.range[0], args.range[1], args.point))
            prod_d[dynamo.session_id] = dynamo.prod_sum()
        client.module_send_production(prod_d)
