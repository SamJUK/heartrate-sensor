#/usr/bin/env python3

import asyncio
import bleak

FENIX = '14:13:0B:27:FE:64'
INSTINCT = 'D6:68:49:D4:A9:89'
ADDR = FENIX

def processHeartrate(sender, data):
    [flags, hr] = data

    pretty_bits = '{0:08b}'.format(flags)
    BIT_HRV_FORMAT = flags & 1
    BIT_SENSOR_CONTACT_FEATURE = (flags >> 2) & 1
    BIT_SENSOR_CONTACT_STATUS = (flags >> 1) & 1
    BIT_ENERGY_EXPENDED_STATUS = (flags >> 3) & 1
    BIT_RR_INTERVAL = (flags >> 4) & 1

    HRV_FORMAT = 'UINT8' if BIT_HRV_FORMAT == 0 else 'UINT16'
    SENSOR_CONTACT_FEATURE = 'Unsupported' if BIT_SENSOR_CONTACT_FEATURE == 0 else 'Supported'
    SENSOR_CONTACT_STATUS = 'No/Bad Contact' if BIT_SENSOR_CONTACT_STATUS == 0 else 'Good Contact'
    ENERGY_EXPENDED_STATUS = 'Not Present' if BIT_ENERGY_EXPENDED_STATUS == 0 else 'Present'
    RR_INTERVAL = 'Not Present' if BIT_RR_INTERVAL == 0 else 'Present'

    if BIT_SENSOR_CONTACT_FEATURE != 0 and BIT_SENSOR_CONTACT_STATUS == 0:
        hr = '-'

    print(f'♥ {hr}')
    print(pretty_bits)
    print(f'{BIT_HRV_FORMAT} : HRV Format : {HRV_FORMAT}')
    print(f'{BIT_SENSOR_CONTACT_FEATURE} : BIT_SENSOR_CONTACT_FEATURE : {SENSOR_CONTACT_FEATURE}')
    print(f'{BIT_SENSOR_CONTACT_STATUS} : BIT_SENSOR_CONTACT_STATUS : {SENSOR_CONTACT_STATUS}')
    print(f'{BIT_ENERGY_EXPENDED_STATUS} : ENERGY_EXPENDED_STATUS : {ENERGY_EXPENDED_STATUS}')
    print(f'{BIT_RR_INTERVAL} : RR_INTERVAL : {RR_INTERVAL}')
    print('---------------')

async def main(ADDR):
    print('Watching Address: {}'.format(ADDR))
    async with bleak.BleakClient(ADDR, timeout=10) as client:
        print('> Connected.')
        await client.start_notify('00002a37-0000-1000-8000-00805f9b34fb', processHeartrate)
        await asyncio.sleep(120)
        await client.stop_notify('00002a37-0000-1000-8000-00805f9b34fb')

asyncio.run(main(ADDR))