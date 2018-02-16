import sys
import requests
import random
import argparse
import threading

# Create file config/master.py following template.py in the same folder
from config.master import *

class Dynamo:
    def __init__(self, address, uuid, **kwargs):
        self.mutex = threading.Lock()
        self.address = address
        self.uuid = uuid
        self.session_id = None
        self.t_prod = set()
        return super().__init__(**kwargs)

    def prod_sum(self) -> float:
        self.mutex.acquire(blocking=True)
        mem =  sum(self.t_prod)
        self.t_prod.clear()
        self.mutex.release()
        return mem

    def add_prod(self, prod: float) -> None:
        self.mutex.acquire(blocking=True)
        self.t_prod.add(prod)
        self.mutex.release()


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
        self.base_url = SERVER_URL
        self.api_key = api_key
        self.timeout = 1

    def get_module_id(self, mlists: list) -> dict:
        try:
            resp = requests.post(
                "{}{}".format(self.base_url, "module/get/ids"),
                json=
                {
                    'apiKey': self.api_key,
                    'UUID': mlists
                },
                timeout=self.timeout)
            resp.raise_for_status()
        except Exception as ex:
            print("Something happened")
            return None
        jresp = resp.json()
        #if jresp["status"] == "ko":
        #    ## Handle that error
        #    print(jresp["reason"])
        #    return None
        #if isinstance(jresp["id"], dict):
        #    return jresp["id"]
        if jresp["code"] != "GENERIC_OK":
            return None
        return jresp["moduleIDS"]

    def module_send_production(self, prod_d: dict) -> dict:
        try:
            resp = requests.post(
                "{}{}".format(self.base_url, "module/production/send"),
                json=
                {
                    "apiKey": self.api_key,
                    "production": prod_d
                },
                timeout=self.timeout)
            resp.raise_for_status()
        except Exception as ex:
            print("Something happened")
            return None
        jresp = resp.json()
        if jresp["code"] != "GENERIC_OK":
            return None
        #if jresp["status"] == "ko":
        #    ## Handle that error
        #    print(jresp["reason"])
        #    return None
        return prod_d

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
    client = ClientHandler(API_KEY)
    modules = [
        Dynamo(address, uuid) for address, uuid in
        ((0x2, "001:001:001"), (0x3, "001:001:002"))
        ]
    print("POST .../getModuleId/")
    #id_dict = client.get_module_id(tuple(dynamo.uuid for dynamo in modules))
    #for dynamo in modules:
    #    if dynamo.uuid in id_dict:
    #        dynamo.session_id = id_dict[dynamo.uuid]
    #        print("uuid: {}, session_id {}".format(dynamo.uuid,
    #                                               dynamo.session_id))
    #    else:
    #        print("missing session_id for module {}".format(dynamo.uuid))
    id_list = client.get_module_id(tuple(dynamo.uuid for dynamo in modules))
    for it, dynamo in enumerate(modules):
        dynamo.session_id = id_list[it]
        print("uuid: {}, session_id {}".format(dynamo.uuid, dynamo.session_id))
    print("POST .../moduleSendProduction/")
    execution = True
    prod_d = dict()
    while execution:
        prod_d.clear()
        for dynamo in modules:
            dynamo.add_prod(
                random_range(args.range[0], args.range[1], args.point))
            prod_d[dynamo.session_id] = dynamo.prod_sum()
        ret = client.module_send_production(prod_d)
        if ret is None:
            execution = False
        else:
            print(ret)
            ## Do something
            pass
