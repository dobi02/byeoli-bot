import discord
import os
import asyncio
from discord.ext import commands
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv("DISCORD_BOT_TOKEN")


class MyBot(commands.Bot):
    def __init__(self):
        intents = discord.Intents.default()
        intents.message_content = True

        super().__init__(
            command_prefix="!",
            intents=intents,
            help_command=None
        )

    async def setup_hook(self):
        # cogs 폴더 로드
        if os.path.exists('./cogs'):
            for filename in os.listdir('./cogs'):
                if filename.endswith('.py'):
                    try:
                        await self.load_extension(f'cogs.{filename[:-3]}')
                        print(f"🧩 Loaded extension: {filename}")
                    except Exception as e:
                        print(f"⚠️ Failed to load {filename}: {e}")

        # 주의: 글로벌 싱크는 갱신에 최대 1시간이 걸릴 수 있습니다.
        # 개발 중에는 특정 길드에만 싱크하는 것이 좋지만, 편의상 여기에 둡니다.
        await self.tree.sync()
        print("✅ Slash commands synced globally!")

    async def on_ready(self):
        print(f'🤖 Logged in as {self.user} (ID: {self.user.id})')
        await self.change_presence(activity=discord.Game(name="/승률분석 [RiotID]"))


async def main():
    if not TOKEN:
        print("❌ Error: DISCORD_BOT_TOKEN is missing in .env")
        return

    bot = MyBot()
    async with bot:
        await bot.start(TOKEN)


if __name__ == '__main__':
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        pass