from datetime import datetime, timezone

import falcon
import falcon.asgi

from database import db


class DecksResources:
    async def init_db(self):
        await db.initialize()

    async def on_post(self, req, resp, player_id):
        data = await req.get_media()
        current_time = datetime.now(timezone.utc)
        server_time_z = current_time.strftime("%Y-%m-%dT%H:%M:%S.%f")[:-3] + "Z"
        new_deck = {
            'name': data.get("name"),
            'main_faction': data.get("main_faction"),
            'ally_faction': data.get("ally_faction"),
            'deck_code': data.get("deck_code"),
            'modify_date': server_time_z,
        }
        deck = await db.deck_create(user_id=player_id, deck=new_deck)
        resp.media = {
            "name": deck.name,
            "main_faction": deck.main_faction,
            "ally_faction": deck.ally_faction,
            "card_back": deck.card_back,
            "deck_code": deck.deck_code,
            "favorite": deck.favorite,
            "id": deck.id,
            "last_played": str(deck.last_played),
            "create_date": str(deck.create_date),
            "modify_date": str(deck.modify_date),
        }

        resp.state = falcon.HTTP_200

    async def on_put(self, req, resp, player_id):
        data = await req.get_media()
        print(data.get('name'))
        if data.get('action') == 'change_card_back':
            await db.initialize()
            deck = await db.get_deck(id=data.get('id'))
            deck.card_back = data.get('name')
            await deck.save()
        resp.state = falcon.HTTP_200
