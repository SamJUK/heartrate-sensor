#/usr/bin/env python3

import argparse
import asyncio
import bleak

#
# List All Devices
#
async def list_all_devices():
    devices = await bleak.BleakScanner.discover()
    for d in devices:
        print(d)
        


parser = argparse.ArgumentParser(description='Discover all BLE Devices')
config = parser.parse_args()

asyncio.run(list_all_devices())