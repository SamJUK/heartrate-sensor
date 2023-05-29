#/usr/bin/env python3

import sys
import argparse
import asyncio
from bleak import BleakScanner, BleakClient

async def list_all_devices():
    scanner = BleakScanner()
    devices = await scanner.discover()
    for d in devices:
        print(d)

async def discover(addr):
    print('Discovering Address: {}'.format(addr))

    async with BleakClient(addr, timeout=30) as client: 
        print('> Connected.')

        # Print Device Name
        name = await client.read_gatt_char('00002a00-0000-1000-8000-00805f9b34fb')
        print('> Device: {}'.format(name.decode('utf-8')))

        # List Services
        print('Services:')
        for id in client.services.services:
            svc = client.services.get_service(id)
            desc = svc.description
            uuid = svc.uuid
            char_ids = ','.join([str(chr.handle) for chr in svc.characteristics])
            print('  [{}] {} {} ({})'.format(uuid, id, desc, char_ids))

        # List Characteristics
        print('\nCharacteristics: ')
        for id in client.services.characteristics:
            chr = client.services.get_characteristic(id)
            desc = chr.description
            uuid = chr.uuid
            properties_list = ','.join(chr.properties)
            print('  [{}] {} {} ({})'.format(uuid, id, desc, properties_list))

        # List Descriptors
        print('\nDescriptors: ')
        for id in client.services.descriptors:
            desc = client.services.get_descriptor(id)
            des = desc.description
            uuid = desc.uuid
            print('  [{}] {} {}'.format(uuid, id, des))


parser = argparse.ArgumentParser(description='BLE Device Discovery')
parser.add_argument('-d', '--device', help='The device ID to discover')
config = parser.parse_args()

if config.device:
    asyncio.run(discover(config.device))
else:
    asyncio.run(list_all_devices())