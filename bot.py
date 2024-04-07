import env
import logging
from pyrogram import Client, idle
from pyrogram import raw
from pyromod import listen
from pyrogram.errors import ApiIdInvalid, ApiIdPublishedFlood, AccessTokenInvalid, BadMsgNotification

logging.basicConfig(
    level=logging.WARNING, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)

app = Client(
    ":memory:",
    api_id=env.API_ID,
    api_hash=env.API_HASH,
    bot_token=env.BOT_TOKEN,
    plugins=dict(root="StringSessionBot"),
)

async def synchronize_time():
    await app.send(raw.functions.updates.GetState())

async def start_bot():
    print("Starting the bot")
    try:
        await app.start()
        # await synchronize_time()  # Comment out or remove this line
    except (ApiIdInvalid, ApiIdPublishedFlood):
        raise Exception("Your API_ID/API_HASH is not valid.")
    except AccessTokenInvalid:
        raise Exception("Your BOT_TOKEN is not valid.")
    except BadMsgNotification as e:
        print(f"BadMsgNotification error: {e}")
        # Handle the error appropriately

    # Client has been started, can now safely use it
    me = await app.get_me()
    uname = me.username
    print(f"@{uname} is now running!")
    idle()
    app.stop()
    print("Bot stopped. Alvida!")

if __name__ == "__main__":
    import asyncio
    asyncio.run(start_bot())