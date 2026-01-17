# database.py
from typing import Optional

from tortoise import Tortoise, run_async
from models import User, Decks
from config import DATABASE_URL


class DatabaseManager:
    def __init__(self):
        self.db_url = None
        self._initialized = False

    async def initialize(self, db_url: str = DATABASE_URL) -> bool:  #连接
        self.db_url = db_url

        try:
            await Tortoise.init(
                db_url=self.db_url,
                modules={'models': ['models']}
            )
            self._initialized = True
            print("✅ 数据库连接成功")
            return True
        except Exception as e:
            print(f"❌ 数据库连接失败: {e}")
            return False

    async def close(self):  #断开
        try:
            await Tortoise.close_connections()
            print("✅ 数据库连接已关闭")
        except Exception as e:
            print(f"❌ 数据库断开失败: {e}")

    async def create_tables(self) -> bool:  #表的检查
        if not self._initialized:
            return False
        import warnings
        with warnings.catch_warnings(record=True) as caught_warnings:
            warnings.filterwarnings('ignore', message="Table '.*' already exists")
            await Tortoise.generate_schemas()
        for warning in caught_warnings:
            if "already exists" in str(warning.message):
                print("ℹ️  表已存在，无需创建")
                break
            else:
                print("✅ 表创建成功")
                break
        print("✅ 表结构检查完成")
        return True

    async def create_user(self, username: str, password: str) -> Optional[User]:  #创建新用户
        try:
            user = await User.create(
                username=username,
                password=password,
                player_name="<anon>",
                player_tag=0000
            )
            print(f"✅ 用户创建成功: {username}")
            return user
        except Exception as e:
            print(f"❌ 创建用户失败: {e}")
            return None

    async def get_user(self, **filters) -> Optional[User]:  #查询
        user = await User.get(**filters)
        return user

    async def user_exists(self, **filters) -> bool:
        """检查用户是否存在"""
        if not self._initialized:
            await self.initialize()

        exists = await User.filter(**filters).exists()
        print(f"🔍 用户存在检查: {filters} -> {exists}")
        return exists

    async def updata_user(self, user_id: int, **kwargs) -> bool:  #更新
        try:
            user = await self.get_user(id=user_id)
            if not user:
                return False
            for key, value in kwargs.items():
                if hasattr(user, key):
                    setattr(user, key, value)
            await user.save()
            print(f"✅ 用户更新成功: ID={user_id}")
            return True
        except Exception as e:
            print(f"❌ 更新用户失败: {e}")
            return False
    async def deck_create(self, user_id: int, deck: dict):
        try:
            user = await User.get(id=user_id)
            print(deck)
            d = await Decks.create(
                name=deck.get('name'),
                main_faction=deck.get('main_faction'),
                ally_faction=deck.get('ally_faction'),
                deck_code=deck.get('deck_code'),
                favorite=False,
                card_back='',
                modify_date=deck.get('modify_date'),
                user=user
            )
            print("✅ 创建卡组成功")
            return d
        except Exception as e:
            print(f'❌ 创建卡组失败{e}')


    """
async def deck_find(self, user_id: int):
    try:
        user = await User.get(id=user_id)
        decks = await user.decks
        return decks
    except Exception as e:
        print("❌ 查询卡组失败")
"""

    async def get_deck(self, **filters) -> Optional[Decks]:  #查询
        deck = await Decks.get(**filters)
        return deck


db = DatabaseManager()
