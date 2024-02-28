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

if __name__ == "__main__":
    print("Starting the bot")
    try:
        app.start()

        await synchronize_time()
    except (ApiIdInvalid, ApiIdPublishedFlood):
        raise Exception("Your API_ID/API_HASH is not valid.")
    except AccessTokenInvalid:
        raise Exception("Your BOT_TOKEN is not valid.")
    except BadMsgNotification as e:
        print(f"BadMsgNotification error: {e}")

    uname = app.get_me().username
    print(f"@{uname} is now running!")
    idle()
    app.stop()
    print("Bot stopped. Alvida!")