from datetime import datetime, timezone
import uvicorn
import asyncio
from app import app
from config import *
from websocket import WebSocketServer
import json
from database import db


async def initialize_database():
    """初始化数据库"""
    print("🔄 正在初始化数据库连接...")
    await db.initialize()
    await db.create_tables()
    print("✅ 数据库初始化完成")


async def start_websocket_server():
    """启动WebSocket服务器"""
    websocket_server = WebSocketServer()
    websocket_task = asyncio.create_task(websocket_server.start())

    async def send_data_periodically():  # 定时向WebSocket客户端发送数据
        while True:
            await asyncio.sleep(10)  # 每10秒发送一次ping
            try:
                current_time = datetime.now(timezone.utc)
                server_time_z = current_time.strftime("%Y-%m-%dT%H:%M:%S.%f")[:-3] + "Z"
                await websocket_server.send(json.dumps({
                    "message": "pong",
                    "channel": "ping",
                    "context": "",
                    "timestamp": server_time_z,
                    "sender": 278881,
                    "receiver": ""

                }))
            except Exception as e:
                print(f"WebSocket发送错误: {e}")

    periodic_task = asyncio.create_task(send_data_periodically())
    return websocket_task, periodic_task


async def start_http_server():
    """启动HTTP服务器"""
    config = uvicorn.Config(
        app,
        host=host,
        port=port,
        server_header=False,
        date_header=False,
    )
    server = uvicorn.Server(config)
    await server.serve()


async def main():
    """同时启动HTTP和WebSocket服务器"""
    await initialize_database()
    websocket_task, periodic_task = await start_websocket_server()  # 启动WebSocket服务器
    http_task = asyncio.create_task(start_http_server())  # 启动HTTP服务器
    await asyncio.gather(http_task, websocket_task, periodic_task)  # 等待所有任务完成


def run_servers():
    """运行所有服务器"""
    asyncio.run(main())


if __name__ == '__main__':
    run_servers()
