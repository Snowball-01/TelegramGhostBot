import logging
from pyrogram import Client, __version__
from pyrogram.raw.all import layer
from variables import Vars
from datetime import datetime


# ─── Logging Setup ───
logging.basicConfig(
    format="%(asctime)s | %(levelname)s | %(message)s",
    datefmt="%H:%M:%S",
    level=logging.INFO
)
logger = logging.getLogger("Bot")

# Reduce noise from pyrogram/urllib3/etc
logging.getLogger("pyrogram").setLevel(logging.WARNING)
logging.getLogger("asyncio").setLevel(logging.ERROR)
logging.getLogger("httpx").setLevel(logging.ERROR)


class Bot(Client):
    def __init__(self):
        super().__init__(
            name="account_steal",
            api_id=Vars.API_ID,
            api_hash=Vars.API_HASH,
            bot_token=Vars.BOT_TOKEN,
            plugins=dict(root="handlers")
        )
        self.start_time = datetime.now()

    async def start(self):
        await super().start()
        me = await self.get_me()
        self.mention = me.mention
        self.username = me.username

        # ─── Clean Startup Logs ───
        logger.info("🚀 Bot is now online!")
        logger.info(f"🤖 Logged in as: {me.first_name} (@{me.username})")
        logger.info(f"📚 Pyrogram v{__version__} | Layer {layer}")
        logger.info(
            f"🕒 Uptime started: {self.start_time.strftime('%d-%m-%Y %I:%M:%S %p')}")

        # Inform admins
        for admin_id in Vars.ADMINS:
            try:
                await self.send_message(
                    admin_id,
                    f"✅ **{me.first_name}** is now online!\n\n"
                    f"🕒 Started at: `{self.start_time.strftime('%d-%m-%Y %I:%M:%S %p')}`\n"
                    f"📚 Version: `Pyrogram v{__version__} | Layer {layer}`"
                )
            except Exception:
                logger.warning(
                    f"⚠️ Couldn’t send start message to admin ID: {admin_id}")

    async def stop(self, *args):
        await super().stop()
        logger.info("☠️ Bot stopped. Goodbye!")


Bot().run()
