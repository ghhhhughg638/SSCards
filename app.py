import falcon
import falcon.asgi

from resources import *

"""
class PathRewriteMiddleware:
    async def process_request(self, req, resp):
        # 将 // 开头的路径重写为 /
        print('???')
        if req.path.startswith('//'):
            print('开始移除')
            req.path = req.path[1:]  # 移除一个斜杠
            print(req.path)
"""

# 创建应用并添加中间件
app = falcon.asgi.App()  #middleware=[PathRewriteMiddleware()])

app.add_route('/.com/config', ConfigResource())
app.add_route('/', RootResource())
app.add_route('/session', SessionResource())
app.add_route('/items/{player_id}', ItemResource())
app.add_route('/players/{player_id}', PlayersResource())
app.add_route('/players/{player_id}/librarynew', LibraryNewResource())
app.add_route('/matches/v2/reconnect', ReConnectResource())
app.add_route('/players/{player_id}/heartbeat', HeartBeatResource())
app.add_route('/store/v2/', XsollaResource())
app.add_route('/fp/', FPResource())
app.add_route('/players/{player_id}/packs', PacksResource())
app.add_route('/players/{player_id}/friends', FriendResource())
app.add_route('/players/{player_id}/decks', DecksResources())
app.add_route('/players/{player_id}/decks/{deck_id}', DeckUpdataResources())
