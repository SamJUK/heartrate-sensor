import json
from datetime import datetime, UTC
from lib.uids import CHAR_HR_MEASUREMENT
from lib.logger import Logger
from bleak import BleakClient
from bleak.exc import BleakError


class Client:
    client = None

    def __init__(self):
        self.logger = Logger(name='client')

    async def connect(self, device):
        self.logger.info(f'Connecting to device: {device}')
        self.client = BleakClient(device, timeout=10)
        try:
            await self.client.connect()
        except BleakError as e:
            self.logger.error(f'Unable to connect to device: {e}')
            return False
        self.logger.info(f'Connected to device: {device}')
        return True
    
    async def monitor(self, socket=None, cb=None):
        self.socket = socket
        self.cb = cb
        if self.client != None:
            await self.client.start_notify(CHAR_HR_MEASUREMENT, self.process)

    async def stopMonitor(self):
        if self.client != None:
            await self.client.stop_notify(CHAR_HR_MEASUREMENT)
            self.logger.log(f'Stopped Monitoring {self.client.address}')

    async def disconnect(self):
        if self.client != None:
            device = self.client.address
            await self.client.disconnect()
            self.logger.log(f'Disconnected from Device: {device}')

    async def process(self, sender, data):
        [flagByte, heartRate] = list(data)
        
        flags = self.processFlags(flagByte)
        if self.isBadHRReading(flags):
            self.logger.warn(f'Received a bad reading from device: {self.client.address}')
            heartRate = '-'

        payload = {
            'device_id': self.client.address,
            'date': datetime.now(UTC).strftime('%Y-%m-%dT%H:%M:%SZ'),
            'hr': str(heartRate)
        }
            
        if self.cb is not None:
            await self.cb(payload)
        elif self.socket is not None:
            if self.socket.closed:
                await self.stopMonitor()
                await self.disconnect()
            else:
                payload['action'] = 'hr'
                await self.socket.send(json.dumps(payload, default=str))

    def processFlags(self, flags):
        return {
            "BIT_HRV_FORMAT": flags & 1,
            "BIT_SENSOR_CONTACT_FEATURE": (flags >> 2) & 1,
            "BIT_SENSOR_CONTACT_STATUS": (flags >> 1) & 1,
            "BIT_ENERGY_EXPENDED_STATUS": (flags >> 3) & 1,
            "BIT_RR_INTERVAL": (flags >> 4) & 1
        }

    def isBadHRReading(self, flags):
        return flags['BIT_SENSOR_CONTACT_FEATURE'] == 1 and flags['BIT_SENSOR_CONTACT_STATUS'] == 0
    
    def describe(self):
        if self.client == None:
            self.logger.warn('Not connected to a client')
            return None

        services = []
        for id in self.client.services.services:
            svc = self.client.services.get_service(id)
            desc = svc.description
            uuid = svc.uuid
            char_ids = ','.join([str(chr.handle) for chr in svc.characteristics])
            services.append('  [{}] {} {} ({})'.format(uuid, id, desc, char_ids))


        characteristics = []
        print('\nCharacteristics: ')
        for id in self.client.services.characteristics:
            chr = self.client.services.get_characteristic(id)
            desc = chr.description
            uuid = chr.uuid
            properties_list = ','.join(chr.properties)
            characteristics.append('  [{}] {} {} ({})'.format(uuid, id, desc, properties_list))

        descriptors = []
        for id in self.client.services.descriptors:
            desc = self.client.services.get_descriptor(id)
            des = desc.description
            uuid = desc.uuid
            descriptors.append('  [{}] {} {}'.format(uuid, id, des))

        return {
            'services': services,
            'characteristics': characteristics,
            'descriptors': descriptors
        }