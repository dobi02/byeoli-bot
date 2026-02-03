import discord
import os
import asyncio
from discord.ext import commands
from dotenv import load_dotenv

# 환경변수 로드
load_dotenv()
TOKEN = os.getenv("DISCORD_BOT_TOKEN")


class MyBot(commands.Bot):
    def __init__(self):
        # Intents 설정 (봇이 서버에서 볼 수 있는 권한)
        intents = discord.Intents.default()
        intents.message_content = True

        super().__init__(
            command_prefix="!",
            intents=intents,
            help_command=None
        )

    async def setup_hook(self):
        # cogs 폴더의 모든 확장 기능 로드
        for filename in os.listdir('./cogs'):
            if filename.endswith('.py'):
                await self.load_extension(f'cogs.{filename[:-3]}')

        # 슬래시 명령어 동기화 (봇 켤 때 서버에 명령어 등록)
        await self.tree.sync()
        print("✅ Slash commands synced!")

    async def on_ready(self):
        print(f'🤖 Logged in as {self.user} (ID: {self.user.id})')
        # 상태 메시지 변경 (예: /승률분석 입력 대기 중...)
        await self.change_presence(activity=discord.Game(name="/승률분석 입력"))


async def main():
    bot = MyBot()
    async with bot:
        await bot.start(TOKEN)


if __name__ == '__main__':
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        # Ctrl+C로 종료 시 깔끔하게
        pass