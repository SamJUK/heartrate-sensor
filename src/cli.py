import json
import argparse
import asyncio

from lib.scanner import Scanner
from lib.client import Client

from outputs.stdout import Stdout
from outputs.file import File

class CLI:
    ACTION_SCAN = 'scan'
    ACTION_MONITOR = 'monitor'
    ACTION_DESCRIBE = 'describe'
    AVAILABLE_ACTIONS = [ACTION_SCAN, ACTION_MONITOR, ACTION_DESCRIBE]

    OUTPUT_FILE=File
    OUTPUT_STDOUT=Stdout
    AVAILABLE_OUTPUTS={
        OUTPUT_FILE.id: OUTPUT_FILE,
        OUTPUT_STDOUT.id: OUTPUT_STDOUT,
    }

    def __init__(self):
        self.config = self.configureArgParse()
        self.output = self.AVAILABLE_OUTPUTS[self.config.output]()

    def configureArgParse(self):
        parser = argparse.ArgumentParser(description='Heart Rate Monitor')
        parser.add_argument('action', choices=self.AVAILABLE_ACTIONS)
        parser.add_argument('-d', '--device', required=False, help='The device ID to monitor')
        parser.add_argument('-o', '--output', default=self.OUTPUT_STDOUT.id, required=False, help='Output Type', choices=self.AVAILABLE_OUTPUTS.keys())
        return parser.parse_args()

    async def execute(self):
        return await getattr(self, self.config.action)()
    
    async def scan(self):
        devices = await Scanner().HRDevices()
        print('\n')
        for device in devices:
            print(f'{devices[device]} - {device}')

    async def describe(self):
        print('Describing Device')
        client = Client()
        await client.connect(self.config.device)
        data = client.describe()
        for section in data:
            print(section)
            for item in data[section]:
                print('  ' + item)

    async def monitor(self):
        client = Client()
        await client.connect(self.config.device)
        await client.monitor(cb=self.output.execute)
        while True:
            await asyncio.sleep(1)
        
if __name__ == '__main__':
    asyncio.run(CLI().execute())