import discord
from discord import app_commands
from discord.ext import commands
import aiohttp
import os


class Prediction(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.api_url = os.getenv("API_SERVER_URL")

    @app_commands.command(name="승률분석", description="소환사의 현재 게임 승률을 예측합니다.")
    @app_commands.describe(summoner_name="소환사 이름 (Riot ID)")
    async def predict(self, interaction: discord.Interaction, summoner_name: str):

        # 1. 일단 응답 지연 (생각 중...) 표시
        await interaction.response.defer(thinking=True)

        try:
            # --- [나중에 API 서버 연결 시 활성화할 부분] ---
            # async with aiohttp.ClientSession() as session:
            #     payload = {"summoner_name": summoner_name}
            #     async with session.post(self.api_url, json=payload) as response:
            #         if response.status == 200:
            #             result = await response.json()
            #             # 여기서 결과 처리...
            #         else:
            #             await interaction.followup.send("API 서버 오류입니다.")
            #             return

            # --- [임시: API 없이 테스트용 응답] ---
            # 실제 서버가 없어도 봇이 작동하는지 확인하기 위함
            await interaction.followup.send(f"🤖 **{summoner_name}** 님의 승률 분석 요청을 받았습니다!\n(아직 API 서버와 연결되지 않았습니다.)")

        except Exception as e:
            await interaction.followup.send(f"🚫 에러 발생: {str(e)}")


async def setup(bot):
    await bot.add_cog(Prediction(bot))