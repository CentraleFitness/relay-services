import sys
import random
import argparse
import time

# Create file config/master.py following template.py in the same folder
from config.master import *
import utils.logger as logger
from hardware.dynamo import Dynamo
from network.client_handler import ClientHandler


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
    parser.add_argument('-silent',
                        help="Silent the log on the standard output",
                        action="store_true")
    parser.add_argument('--level',
                        help="Debug level",
                        type=str,
                        action='store',
                        default='warning')
    args = parser.parse_args()
    log = logger.Logger()
    log.level = args.level
    log.add_gelf_handler(SERVER_IP,
                         GELF_INPUT_PORT,
                         localname="cf-hotspot-003",
                         debugging_fields=False)
    client = ClientHandler(API_KEY)
    modules = [
        Dynamo(address, uuid) for address, uuid in
        ((0x2, "001:001:001"), (0x3, "001:001:002"))
        ]
    print("POST .../module/get/ids")
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
    print("POST .../module/production/send")
    execution = True
    prod_d = dict()
    while execution:
        prod_d.clear()
        for dynamo in modules:
            dynamo.add_prod(
                random_range(args.range[0], args.range[1], args.point))
            prod_d[dynamo.uuid] = dynamo.prod_sum()
        print(prod_d)
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
            ## Do something
            pass
