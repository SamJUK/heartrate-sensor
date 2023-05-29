#/usr/bin/env python3

import sys
import argparse
import asyncio
from bleak import BleakScanner, BleakClient
from bleak.uuids import normalize_uuid_str

UUID_SVC_HR_MONITOR = normalize_uuid_str('180D')

async def list_devices(svc_filter=[]):
    devices_found = False
    async with BleakScanner() as scanner:
        await scanner.discover()
        devices = scanner.discovered_devices_and_advertisement_data 
        for device_id in devices:
            [BLEDevice, Advert] = devices[device_id]
            hasNoSvcFilters = isinstance(svc_filter, list) and len(svc_filter) < 1
            svcFilterMatches = list(set(Advert.service_uuids).intersection(svc_filter))
            if hasNoSvcFilters or len(svcFilterMatches) > 0:
                devices_found = True
                print(f'{device_id} {BLEDevice.name}')

    if devices_found == False:
        print('No Devices Found')

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
parser.add_argument('--list_all', action='store_true', help='List all devices')
config = parser.parse_args()

if config.device:
    asyncio.run(discover(config.device))
elif config.list_all:
    asyncio.run(list_devices())
else:
    asyncio.run(list_devices(svc_filter=[UUID_SVC_HR_MONITOR]))