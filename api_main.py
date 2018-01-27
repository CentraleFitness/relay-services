import requests
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
    def __init__(self):
        self.url = SERVER_URL
        self.timeout = 1

    def get_module_id(self, api_key: str, mlists: list) -> dict:
        try:
            resp = requests.post(
                self.url,
                json=
                {
                    'api_key': api_key,
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

        
if __name__ == "__main__":
    client = ClientHandler()
    modules = [
        Dynamo(address, uuid) for address, uuid in
        ((0x2, "001:001:001"), (0x3, "001:001:002"))
        ]

    api_key = "0001-2083-a4b2-c00f"

    print("POST /getModuleId")
    id_dict = client.get_module_id(api_key, (dynamo.uuid for dynamo in modules))
    for dynamo in modules:
        if dynamo.uuid in id_dict:
            dynamo.session_id = id_dict[dynamo.uuid]
            print("uuid: {}, session_id {}".format(dynamo.uuid,
                                                   dynamo.session_id))
        else:
            print("missing session_id for module {}".format(dynamo.uuid))

