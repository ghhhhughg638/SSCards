# app.py
import falcon
import falcon.asgi


class PlayersResource:
    async def on_put(self, req, resp, player_id):
        resp.media = {"player_name": "核弹爆炸了",
                      "player_tag": 4312}
        resp.status = falcon.HTTP_200
