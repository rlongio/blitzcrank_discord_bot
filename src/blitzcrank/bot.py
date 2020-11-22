import os
from discord.ext import commands
from discord.utils import get
from dotenv import load_dotenv
import logging
from blitzcrank.cogs.admin_utilities import AdminUtilities
from blitzcrank.cogs.permissions import Permissions
from blitzcrank.cogs.welcome import Welcome
from blitzcrank.cogs.youtube_updates import YouTube


def main():
    load_dotenv()
    TOKEN = os.getenv("DISCORD_TOKEN")
    GUILD = os.getenv("DISCORD_GUILD")
    CLIENT_ID = os.getenv("DISCORD_CLIENT_ID")

    logger = logging.getLogger("blitzcrank")
    logger.setLevel(logging.DEBUG)
    handler = logging.FileHandler(filename="blitzcrank.log", encoding="utf-8", mode="w")
    handler.setFormatter(
        logging.Formatter("%(asctime)s:%(levelname)s:%(name)s: %(message)s")
    )
    logger.addHandler(handler)

    bot = commands.Bot(command_prefix="!")

    @bot.event
    async def on_ready() -> None:
        logger.info("We have logged in as {0.user}".format(bot))

    bot.add_cog(Welcome(bot))
    bot.add_cog(YouTube(bot))
    bot.add_cog(Permissions(bot))
    bot.add_cog(AdminUtilities(bot, CLIENT_ID))
    bot.run(TOKEN)


if __name__ == "__main__":
    main()
