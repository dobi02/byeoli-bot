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
        
        # 1. 생각 중 표시
        await interaction.response.defer(thinking=True)

        try:
            async with aiohttp.ClientSession() as session:
                payload = {"summoner_name": summoner_name}
                # 타임아웃 10초
                timeout = aiohttp.ClientTimeout(total=10)
                
                # API 요청 전송
                async with session.post(self.api_url, json=payload, timeout=timeout) as response:
                    
                    if response.status == 200:
                        # 2. 성공 시: API가 준 데이터를 꺼내서 보여줌
                        data = await response.json()
                        
                        # API에서 준 값 (win_rate 등) 확인
                        win_rate = data.get("win_rate", 0.0)
                        team_color = data.get("team_color", "Blue")
                        
                        # 예쁜 결과 메시지 전송
                        await interaction.followup.send(
                            f"🎮 **{summoner_name}** 님 승률 분석 결과\n"
                            f"팀: **{team_color}**\n"
                            f"예측 승률: **{win_rate * 100:.1f}%**"
                        )
                    
                    else:
                        # 3. 실패 시
                        await interaction.followup.send(f"⚠️ 분석 실패 (서버 에러 {response.status})")

        except Exception as e:
            await interaction.followup.send(f"🚫 에러 발생: {str(e)}")

async def setup(bot):
    await bot.add_cog(Prediction(bot))
