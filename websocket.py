import asyncio
import websockets
from config import host, ws_port


class WebSocketServer:
    def __init__(self, host_ws=host, port=ws_port):
        self.host = host_ws
        self.port = port
        self.clients = set()

    async def handle_client(self, websocket):
        self.clients.add(websocket)  # 新的客户端连接
        try:
            async for message in websocket:
                print(f"收到消息: {message}")
        except websockets.ConnectionClosed as e:
            print(f"客户端断开连接: {e}")
        finally:
            self.clients.remove(websocket)  # 移除断开的客户端

    async def send(self, message):
        """向所有连接的客户端发送消息"""
        if not self.clients:
            print("没有客户端连接，无法发送消息")
            return
        disconnected_clients = set()
        for client in self.clients:
            try:
                await client.send(message)
            except websockets.ConnectionClosed:
                disconnected_clients.add(client)
        self.clients -= disconnected_clients  # 清理已断开的客户端

    async def start(self):
        print(f"启动 WebSocket 服务器: ws://{self.host}:{self.port}")
        async with websockets.serve(self.handle_client, self.host, self.port):
            await asyncio.Future()  # 持续运行直到手动停止
