#/usr/bin/env python3

from uuids import CHAR_DEVICE_NAME, CHAR_HR_MEASUREMENT
import argparse
import asyncio
from datetime import datetime
from bleak import BleakClient
from bleak.exc import BleakError

lastUpdate = datetime.now().timestamp()
monitoring = True
config = None
fh = None

def parseArguments():
    global config
    parser = argparse.ArgumentParser(description='Heart Rate Monitor')
    parser.add_argument('-d', '--device', required=True, help='The device ID to monitor')
    parser.add_argument('--file', action='store_true', help='Should write to file')
    parser.add_argument('--file_path', default='./out/hr.csv', help='Where should we write this file?')
    parser.add_argument('--keep_history', action='store_true', help='Keep HR History in output file')
    parser.add_argument('-v', '--verbose', action='store_true', help='Verbose Logging')
    config = parser.parse_args()

def verbose(message):
    if config.verbose:
        print(f'> {message}')

def setupFile():
    if config.file:
        global fh
        mode = 'a' if config.keep_history else 'w' 
        fh = open(config.file_path, mode)

async def printDeviceName(client):
    name = await client.read_gatt_char(CHAR_DEVICE_NAME)
    print('> Device: {}'.format(name.decode('utf-8')))

def processFlags(flags):
    return {
        "BIT_HRV_FORMAT": flags & 1,
        "BIT_SENSOR_CONTACT_FEATURE": (flags >> 2) & 1,
        "BIT_SENSOR_CONTACT_STATUS": (flags >> 1) & 1,
        "BIT_ENERGY_EXPENDED_STATUS": (flags >> 3) & 1,
        "BIT_RR_INTERVAL": (flags >> 4) & 1
    }

def isBadHRReading(flags):
    return flags['BIT_SENSOR_CONTACT_FEATURE'] == 1 and flags['BIT_SENSOR_CONTACT_STATUS'] == 0

def processHeartrate(sender, data):
    global lastUpdate
    lastUpdate = datetime.now().timestamp()

    [flagByte, heartRate] = list(data)
    flags = processFlags(flagByte)
    if isBadHRReading(flags):
        heartRate = '-'

    dt = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    print(f'[{dt}] ♥ {heartRate}')

    if fh != None:
        fh.write(f'{heartRate}\n')
        fh.flush()

async def monitorHR(client):
    verbose(f'Starting Notify for HR Measurement: {CHAR_HR_MEASUREMENT}')
    await client.start_notify(CHAR_HR_MEASUREMENT, processHeartrate)

    hasRecentUpdate = True
    while hasRecentUpdate:
        lastUpdateAgo = datetime.now().timestamp() - lastUpdate
        hasRecentUpdate = lastUpdateAgo < 10
        
        verbose(f'Sleeping: {CHAR_HR_MEASUREMENT}')
        await asyncio.sleep(5.0)

    verbose(f'Stopping Notify for HR Measurement: {CHAR_HR_MEASUREMENT}')
    await client.stop_notify(CHAR_HR_MEASUREMENT)


async def main():
    print('Watching Address: {}'.format(config.device))
    async with BleakClient(config.device, timeout=10) as client:
        print('> Connected.')
        try:
            await printDeviceName(client)
        except BleakError: 
            pass

        while monitoring:
            await monitorHR(client)


try:
    parseArguments()
    setupFile()
    asyncio.run(main())
finally:
    if fh != None:
        fh.close()