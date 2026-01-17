import falcon
import falcon.asgi
from resources.library import library


class LibraryNewResource:
    async def on_get(self, req, resp, player_id):
        resp.media = library
        resp.status = falcon.HTTP_200
