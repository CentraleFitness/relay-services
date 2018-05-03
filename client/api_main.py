"""
    api_main
"""

import json
import random
import argparse
import time

from utils import Pid
from logging import getLogger
from logging.config import dictConfig
from peripheral import Dynamo
from network import ClientHandler

random.seed()

def random_range(floor: float, ceil: float, point: int) -> float:
    """
        Create a 'random' value between the given values
        args:
            floor: The minimum value
            ceil: The maximum value
            point: The number of decimals after the floating point
    """
    return round(random.uniform(floor, ceil), point)

def main():
    """
        main
    """
    my_pid = Pid("cf_client_api")
    assert not my_pid.is_running()
    my_pid.set_pidfile()


    parser = argparse.ArgumentParser(description="API communication experiment")
    parser.add_argument('--range', '-r',
                        help="Production range (in Watt)",
                        nargs=2,
                        metavar=('min', 'max'),
                        type=float,
                        action='store',
                        default=(1, 5))
    parser.add_argument('--point', '-p',
                        help="Number of digits after the floating point",
                        type=int,
                        action='store',
                        default=2)
    parser.add_argument('-s', '--settings',
                        help="path to the json config file",
                        type=str,
                        action='store',
                        default='./settings.json')
    args = parser.parse_args()
    with open(args.settings, 'r') as fhandler:
        data = json.load(fhandler)
    dictConfig(data['logging_dict'])
    logger = getLogger(__name__)
    client = ClientHandler(data['server']['api_url'], data['server']['api_key'])
    modules = [Dynamo(0x01, "001:001:001")]
    logger.info("Program started")
    id_list = client.get_module_id(tuple(dynamo.uuid for dynamo in modules))
    for it, dynamo in enumerate(modules):
        dynamo.session_id = id_list[it]
    # TODO
    logger.info("Initialisation done. Send production NOW.")
    execution = True
    prod_d = dict()
    while execution:
        prod_d.clear()
        for dynamo in modules:
            dynamo.add_prod(
                random_range(args.range[0], args.range[1], args.point))
            prod_d[dynamo.uuid] = dynamo.prod_sum()
        logger.debug(prod_d)
        ret = client.module_send_production(prod_d)
        time.sleep(1)
        if ret is None:
            execution = False
        else:
            for command in ret:
                if command["cmd"] == "setModuleId":
                    for param in command["params"]:
                        for dynamo in modules:
                            if dynamo.uuid == param['UUID']:
                                dynamo.session_id = param["moduleID"]

if __name__ == "__main__":
    main()
