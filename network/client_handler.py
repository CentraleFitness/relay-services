"""
    Client Handler
    Status: OK
    Protocol version: 1.0
"""

import requests
import utils.logger as logger

from config.master import *

class ClientHandler:
    """
    Send requests to the main server
    """
    def __init__(self, api_key):
        """
        args:
            api_key: The API key to authenticate to the server
        """
        self.base_url = SERVER_URL
        self.api_key = api_key
        self.timeout = 30

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
            logger.error("Exception handled: {}".format(ex))
            return None
        jresp = resp.json()
        #if jresp["status"] == "ko":
        #    ## Handle that error
        #    print(jresp["reason"])
        #    return None
        #if isinstance(jresp["id"], dict):
        #    return jresp["id"]
        if jresp["code"] != "GENERIC_OK":
            logger.error("KO: Error code {}".format(jresp['code']))
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
            logger.error("Exception handled: {}".format(ex))
            return None
        jresp = resp.json()
        if jresp["code"] != "GENERIC_OK":
            logger.error("KO: Error code {}".format(jresp['code']))
            return None
        return jresp.get("commande", [])
        #if jresp["status"] == "ko":
        #    ## Handle that error
        #    print(jresp["reason"])
        #    return None
