#!/usr/bin/env python

import json
import asyncio
import argparse
from websockets.server import serve

from lib.scanner import Scanner
from lib.client import Client
from lib.logger import Logger

parser = argparse.ArgumentParser(description='Websocket Server - Heart Rate Monitor')
parser.add_argument('-H', '--host', type=str, help='Server Host', default="0.0.0.0")
parser.add_argument('-P', '--port', type=str, help='Server Port', default=8765)
config = parser.parse_args()

logger = Logger()

async def handler(websocket):
    logger.info(f'Websocket Connection Received: {websocket.id}')

    clients = {}

    while websocket.closed == False:
        async for message in websocket:
            if message == 'scan':
                devices = await Scanner().HRDevices()
                await websocket.send(json.dumps({
                    'action': 'devices',
                    'devices': devices
                }))
            elif message.startswith('connect:'):
                [action, device] = message.split(':')
                clients[device] = Client()
                if await clients[device].connect(device):
                    await clients[device].monitor(socket=websocket)
                else:
                    await websocket.send(json.dumps({
                        'error': 'Unable to connect to device'
                    }))
            elif message.startswith('disconnect:'):
                [action, device] = message.split(':')
                await clients[device].stopMonitor()
                await clients[device].disconnect()
        await asyncio.sleep(1)
    logger.info(f'Websocket Closed: {websocket.id}')

async def main():
    async with serve(handler, config.host, config.port):
        logger.info('Started the Websocket Server at ws://{}:{}'.format(config.host, config.port))
        await asyncio.Future()  # run forever

asyncio.run(main())