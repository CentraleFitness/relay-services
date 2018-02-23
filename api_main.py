import sys
import random
import argparse
import time

# Create file config/master.py following template.py in the same folder
from config.master import *
import utils.logger as mlogger
from hardware.dynamo import Dynamo
from network.client_handler import ClientHandler


def random_range(floor: float, ceil: float, point: int) -> float:
    return round(random.uniform(floor, ceil), point)
        
def main():
    random.seed()
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
    args = parser.parse_args()
    client = ClientHandler(API_KEY)
    modules = [
        Dynamo(address, uuid) for address, uuid in
        ((0x2, "001:001:001"), (0x3, "001:001:002"))
        ]
    logger.info("Program started")
    #id_dict = client.get_module_id(tuple(dynamo.uuid for dynamo in modules))
    #for dynamo in modules:
    #    if dynamo.uuid in id_dict:
    #        dynamo.session_id = id_dict[dynamo.uuid]
    #        print("uuid: {}, session_id {}".format(dynamo.uuid,
    #                                               dynamo.session_id))
    #    else:
    #        print("missing session_id for module {}".format(dynamo.uuid))
    id_list = client.get_module_id(tuple(dynamo.uuid for dynamo in modules))
    if not id_list:
        logger.critical("Empty module ids. Execution stop.")
        return 1
    for it, dynamo in enumerate(modules):
        dynamo.session_id = id_list[it]
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
    return 0

if __name__ == "__main__":
    mlogger.dict_config(LOGGING_DICT)
    logger = mlogger.get_logger(__name__)
    ret = main()
    if ret == 0:
        logger.info("Program stopped without any problem")
    else:
        logger.critical(
            """
            An error occured and cause the program to stop.
            Return code {}
            """.format(ret))
