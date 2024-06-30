from lib.uids import SVC_HR_MEASUREMENT
from lib.logger import Logger
from bleak import BleakScanner

class Scanner:
    def __init__(self):
        self.logger = Logger(name='scan')

    async def devices(self, svc_filter=[]):
        self.logger.info(f'Scanning for devices: svc_filter={svc_filter}')
        found_devices = {}
        async with BleakScanner() as scanner:
            await scanner.discover()
            devices = scanner.discovered_devices_and_advertisement_data
            for id in devices:
                [BLEDevice, Advert] = devices[id]
                hasNoSvcFilter = isinstance(svc_filter, list) and len(svc_filter) < 1
                svcFilterMatches = list(set(Advert.service_uuids).intersection(svc_filter))
                if hasNoSvcFilter or len(svcFilterMatches) > 0:
                    found_devices[id] = BLEDevice.name

        self.logger.info(f'Found Devices: {found_devices}')
        return found_devices
    
    async def HRDevices(self):
        return await self.devices(svc_filter=[SVC_HR_MEASUREMENT])
