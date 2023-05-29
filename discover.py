#/usr/bin/env python3

import sys
import asyncio
import bleak

def getDeviceId():
    device_id = str(sys.argv[1])
    if len(device_id) < 1:
        print('[ERR]: No Device ID Presented')
        sys.exit(1)
    return device_id

async def discover(addr):
    print('Discovering Address: {}'.format(addr))

    async with bleak.BleakClient(addr, timeout=30) as client:
        print('> Connected.')

        # List Services
        print('Services:')
        for id in client.services.services:
            svc = client.services.get_service(id)
            desc = svc.description
            uuid = svc.uuid
            print('  [{}] {} {}'.format(uuid, id, desc))
            print(','.join([str(chr.handle) for chr in svc.characteristics]))

        # List Characteristics
        print('\nCharacteristics: ')
        for id in client.services.characteristics:
            chr = client.services.get_characteristic(id)
            desc = chr.description
            uuid = chr.uuid
            print('  [{}] {} {}'.format(uuid, id, desc))
            for property in chr.properties:
                print('    - {}'.format(property))

        # List Descriptors
        print('\nDescriptors: ')
        for id in client.services.descriptors:
            desc = client.services.get_descriptor(id)
            des = desc.description
            uuid = desc.uuid
            print('  [{}] {} {}'.format(uuid, id, des))


asyncio.run(discover(getDeviceId()))