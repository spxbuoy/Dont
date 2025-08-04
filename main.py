import os
from pyrogram import Client, filters
from pyrogram.types import Message

# --- CONFIGURATION ---
API_ID = int(os.getenv("API_ID", "29954197"))  # replace or set via env
API_HASH = os.getenv("API_HASH", "4ea7a4f028bed2a8077c65085dddc9c4")  # rotate if exposed
BOT_TOKEN = os.getenv("BOT_TOKEN", "8222967896:AAH75Zv8EWpQ_Z3Ojwaq0_gzTF1Z6m4YU8I")  # rotate if exposed

# --- PREMIUM CONFIG ---
# Put your Telegram numeric user ID(s) here to auto-grant premium.
# Example: AUTO_PREMIUM_IDS = {123456789, 987654321}
AUTO_PREMIUM_IDS = {7941175119}  # <<< replace with your own user ID

# In-memory premium store (you can persist this later if needed)
premium_users = set()
# Dummy allowed sites per user (replace with persistent DB if desired)
user_sites = {}

# Welcome/start message
START_TEXT = """🚀 𝙃𝙚𝙡𝙡𝙤 𝘽𝙪𝙙𝙙𝙮!

📋 𝘼𝙫𝙖𝙞𝙡𝙖𝙗𝙡𝙚 𝘾𝙤𝙢𝙢𝙖𝙣𝙙𝙨

/add 𝙨𝙞𝙩𝙚.𝙘𝙤𝙢 𝙨𝙞𝙩𝙚.𝙘𝙤𝙢 𝙨𝙞𝙩𝙚.𝙘𝙤𝙢
   ↳ 𝙁𝙤𝙧 𝘼𝙙𝙙𝙞𝙣𝙜 𝙈𝙪𝙡𝙩𝙞𝙥𝙡𝙚 𝙐𝙍𝙇𝙨

/info
   ↳ 𝙁𝙤𝙧 𝙂𝙚𝙩𝙩𝙞𝙣𝙜 𝙐𝙨𝙚𝙧 𝙄𝙣𝙛𝙤𝙧𝙢𝙖𝙩𝙞𝙤𝙣

/rm 𝙨𝙞𝙩𝙚.𝙘𝙤𝙢
   ↳ 𝙁𝙤𝙧 𝙍𝙚𝙢𝙤𝙫𝙞𝙣𝙜 𝙖 𝙎𝙞𝙩𝙚 𝙁𝙧𝙤𝙢 𝘿𝙖𝙩𝙖𝙗𝙖𝙨𝙚

/redeem {{key}}
   ↳ 𝙁𝙤𝙧 𝙍𝙚𝙙𝙚𝙚𝙢𝙞𝙣𝙜 𝙋𝙧𝙚𝙢𝙞𝙪𝙢 𝙆𝙚𝙮

/sh 5282480007599832|09|2025|453
   ↳ 𝙁𝙤𝙧 𝙎𝙞𝙣𝙜𝙡𝙚 𝘾𝙖𝙧𝙙 𝘾𝙝𝙚𝙘𝙠 (𝙤𝙧 𝙧𝙚𝙥𝙡𝙮 𝙩𝙤 𝙘𝙖𝙧𝙙)

/msh 5282480007599832|09|2025|453
   ↳ 𝙁𝙤𝙧 𝙈𝙖𝙨𝙨 𝘾𝙖𝙧𝙙 𝘾𝙝𝙚𝙘𝙠 (𝙤𝙧 𝙧𝙚𝙥𝙡𝙮 𝙩𝙤 𝙡𝙞𝙨𝙩)
   
/mtxt
   ↳ 𝙁𝙤𝙧 𝘾𝙝𝙚𝙘𝙠𝙞𝙣𝙜 𝘾𝙖𝙧𝙙𝙨 𝙁𝙧𝙤𝙢 𝙏𝙚𝙭𝙩 𝙁𝙞𝙡𝙚
"""

UNAUTH_MSG = """🚫 𝙐𝙣𝙖𝙪𝙩𝙝𝙤𝙧𝙞𝙨𝙚𝙙 𝘼𝙘𝙘𝙚𝙨𝙨!

𝙔𝙤𝙪 𝙘𝙖𝙣 𝙪𝙨𝙚 𝙩𝙝𝙞𝙨 𝙗𝙤𝙩 𝙞𝙣 𝙜𝙧𝙤𝙪𝙥 𝙛𝙤𝙧 𝙛𝙧𝙚𝙚!

𝙁𝙤𝙧 𝙥𝙧𝙞𝙫𝙖𝙩𝙚 𝙖𝙘𝙘𝙚𝙨𝙨, 𝙘𝙤𝙣𝙩𝙖𝙘𝙩 @𝙈𝙤𝙙_𝘽𝙮_𝙆𝙖𝙢𝙖𝙡
"""

# Instantiate client
app = Client("my_bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)


def is_premium(user_id: int) -> bool:
    return user_id in premium_users or user_id in AUTO_PREMIUM_IDS


# Optionally auto-add the AUTO_PREMIUM_IDS into the in-memory set so they appear if you inspect premium_users
for uid in AUTO_PREMIUM_IDS:
    premium_users.add(uid)


@app.on_message(filters.command("start"))
def start_handler(_, msg: Message):
    msg.reply_text(START_TEXT)


@app.on_message(filters.command("add"))
def add_handler(_, msg: Message):
    if not is_premium(msg.from_user.id):
        return msg.reply_text(UNAUTH_MSG)
    args = msg.command[1:]
    if not args:
        return msg.reply_text("Usage: /add site.com [more sites...]")
    user_sites.setdefault(msg.from_user.id, set()).update(args)
    msg.reply_text(f"Added: {', '.join(args)}")


@app.on_message(filters.command("info"))
def info_handler(_, msg: Message):
    if not is_premium(msg.from_user.id):
        return msg.reply_text(UNAUTH_MSG)
    sites = user_sites.get(msg.from_user.id, set())
    msg.reply_text(f"Your info:\nPremium: ✅\nTracked sites: {', '.join(sites) if sites else 'None'}")


@app.on_message(filters.command("rm"))
def rm_handler(_, msg: Message):
    if not is_premium(msg.from_user.id):
        return msg.reply_text(UNAUTH_MSG)
    args = msg.command[1:]
    if not args:
        return msg.reply_text("Usage: /rm site.com")
    to_remove = args[0]
    user_sites.get(msg.from_user.id, set()).discard(to_remove)
    msg.reply_text(f"Removed: {to_remove}")


@app.on_message(filters.command("redeem"))
def redeem_handler(_, msg: Message):
    if len(msg.command) < 2:
        return msg.reply_text("Usage: /redeem <key>")
    key = msg.command[1]
    # Placeholder logic: any key starting with "PREM" grants premium
    if key.upper().startswith("PREM"):
        premium_users.add(msg.from_user.id)
        msg.reply_text("🎉 Premium activated! You now have access.")
    else:
        msg.reply_text("❌ Invalid key.")


@app.on_message(filters.command("sh"))
def single_card(_, msg: Message):
    if not is_premium(msg.from_user.id):
        return msg.reply_text(UNAUTH_MSG)
    payload = msg.text.split(maxsplit=1)[1] if len(msg.text.split()) > 1 else ""
    msg.reply_text(f"Processing single card: {payload}")


@app.on_message(filters.command("msh"))
def mass_card(_, msg: Message):
    if not is_premium(msg.from_user.id):
        return msg.reply_text(UNAUTH_MSG)
    payload = msg.text.split(maxsplit=1)[1] if len(msg.text.split()) > 1 else ""
    msg.reply_text(f"Processing mass card list: {payload}")


@app.on_message(filters.command("mtxt"))
def mtxt_handler(_, msg: Message):
    if not is_premium(msg.from_user.id):
        return msg.reply_text(UNAUTH_MSG)
    msg.reply_text("Processing cards from text (not implemented).")


@app.on_message(filters.private)
def fallback(_, msg: Message):
    if msg.text and msg.text.startswith("/"):
        msg.reply_text(UNAUTH_MSG)


if __name__ == "__main__":
    print("Bot is starting...")
    app.run()
          
