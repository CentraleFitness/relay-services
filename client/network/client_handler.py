"""
    Client Handler
    Status: OK
    Protocol version: 1.0
"""

import requests
import logging

class ClientHandler:
    """
    Send requests to the main server
    """
    def __init__(self, request_url: str, api_key: str):
        """
        args:
            api_key: The API key to authenticate to the server
        """
        self.base_url = request_url
        self.api_key = api_key
        self.timeout = 30
        self.logger = logging.getLogger(__name__)

    def get_module_id(self, mlists: list) -> list:
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
            self.logger.error("Exception handled: {}".format(ex))
            return None
        jresp = resp.json()
        if jresp["code"] != "GENERIC_OK":
            self.logger.error("KO: Error code {}".format(jresp['code']))
            return None
        id_list = jresp.get('moduleIDS', [])
        if not id_list:
            self.logger.critical("Empty module ids. Execution stop.")
            raise AssertionError
        return id_list

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
            self.logger.error("Exception handled: {}".format(ex))
            return None
        jresp = resp.json()
        if jresp["code"] != "GENERIC_OK":
            self.logger.error("KO: Error code {}".format(jresp['code']))
            return None
        return jresp.get("commande", [])
