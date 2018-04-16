from gattlib import DiscoveryService

service = DiscoveryService("hci0")
devices = service.discover(5)

for address, name in devices.items():
    print("name: {}, address: {}".format(name, address))
