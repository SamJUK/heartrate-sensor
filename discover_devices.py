#/usr/bin/env python3

import asyncio
import bleak

#
# List All Devices
#
async def list_all_devices():
    devices = await bleak.BleakScanner.discover()
    for d in devices:
        print(d)
        
asyncio.run(list_all_devices())