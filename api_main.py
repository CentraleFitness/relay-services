import requests
from config.master import *

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

    api_key = "0001-2083-a4b2-c00f"
    modules = ['001:001:001', '001:001:002', '001:001:002']

    print("POST /getModuleId")
    print("replied: {}", client.get_module_id(api_key, modules))
