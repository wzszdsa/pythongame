import asyncio
import json
from game import *
from const import *
import os, sys
import platform

get_os = platform.system()
split_symbol = "\\" if get_os == "Windows" else '/'
current_path = os.path.abspath(__file__)

top_path = split_symbol.join(current_path.split(split_symbol)[:-2])
sys.path.append(top_path)

from share.const import *

g = Game()


async def main():
    server = await asyncio.start_server(handle_client, '0.0.0.0', LISTEN_PORT)
    print('Server start! Listen on port:', LISTEN_PORT)
    async with server:
        await server.serve_forever()


async def handle_client(reader, writer):
    data = await reader.read(MAX_BYTES)
    msg = json.loads(data.decode())
    print(msg)
    s2cmsg = {}
    if msg['type'] == C2S_ADD_PLANT:
        s2cmsg = g.checkAddPlant(msg['pos'], msg['plant_idx'])
    writer.write(json.dumps(s2cmsg).encode())
    await writer.drain()


asyncio.run(main())
