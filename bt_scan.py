import bluetooth

print("performing inquiry...")
nearby_devices = bluetooth.discover_devices(
        duration=8, lookup_names=True, flush_cache=True, lookup_class=False)

print("found {} devices".format(len(nearby_devices)))
for addr, name in nearby_devices:
    try:
        print(addr, name)
    except UnicodeEncodeError:
        print(addr, name.encode('utf-8'))

