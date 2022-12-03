import logging
import sys
import os.path
import asyncio
from aiohttp import web
from server import BasicServer

log = logging.getLogger()
log.setLevel(logging.DEBUG)
stream = logging.StreamHandler(sys.stdout)
stream.setLevel(logging.DEBUG)
log.addHandler(stream)

clientdir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'client')

class GameServer(BasicServer):
    "Game server"
    
    def __init__(self) -> None:
        super().__init__()

        self.users = {}

    async def handle_message_json(self, data, ws, wsid):
        """Handle incoming messages in json format."""

        await super().handle_message_json(data, ws, wsid)
        await self.send_all_json({'action': 'sent', 'wsid': wsid, 'data': data}, exclude=ws)
        # if data['action'] == 'connect':
        #     await self.onconnect(ws, data)
        # elif data['action'] == 'sent':
        #     await self.onsent(ws, data)
        # elif data['action'] == 'disconnect':
        #     await self.ondisconnect(ws, data)
        # else:
        #     log.warning('Unknown action: %s', data['action'])

    async def handle_connect(self, ws, wsid):
        """Handle client connection."""

        await super().handle_connect(ws, wsid)

        name = (await ws.receive()).data
        self.users[wsid] = {'name': name}

        await ws.send_json({'action': 'connection_established', 'id': wsid, 'users': self.users})
        await self.send_all_json({'action': 'user_connected', 'id': wsid, 'name': name}, exclude=ws)

    async def handle_disconnect(self, ws, wsid):
        """Handle client disconnection."""

        await super().handle_disconnect(ws, wsid)

        del self.users[wsid]

        await self.send_all_json({'action': 'user_disconnected', 'id': wsid})

    def get_routes(self) -> list:
        """Get the routes for the http server"""

        async def handle_index_page(request):
            return web.FileResponse(os.path.join(clientdir, 'index.html'))

        return [
            web.get(
                '/', handle_index_page),
            web.static(
                '/static', os.path.join(clientdir, 'static')),
        ]

if __name__ == "__main__":
    server = GameServer()
    loop = asyncio.get_event_loop()
    loop.run_until_complete(server.start())

    loop.run_forever()
