import discord
from discord import app_commands
from discord.ext import commands
import aiohttp
import os


class Prediction(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        # .env에서 불러오되, 뒤에 엔드포인트 경로까지 정확히 맞춰줍니다.
        base_url = os.getenv("API_SERVER_URL", "http://localhost:8000")
        self.api_url = f"{base_url}/predict/from-discord"

    @app_commands.command(name="승률분석", description="소환사의 현재 게임 승률을 예측합니다.")
    @app_commands.describe(riot_id="소환사 이름 + 태그 (예: Hide on bush#KR1)")
    async def predict(self, interaction: discord.Interaction, riot_id: str):

        # 1. 태그(#) 확인 (Riot ID 필수 조건)
        if "#" not in riot_id:
            await interaction.response.send_message(
                "⚠️ **올바른 형식으로 입력해주세요!**\n예: `Hide on bush#KR1` (이름 뒤에 #태그 필수)",
                ephemeral=True
            )
            return

        await interaction.response.defer(thinking=True)

        try:
            async with aiohttp.ClientSession() as session:
                # API 스펙에 맞는 Payload 구성
                payload = {
                    "riot_id": riot_id,
                    "platform_id": "KR",  # 기본값 한국
                    "use_history": True,
                    "history_count": 20
                }

                # 타임아웃 20초 (데이터 수집에 시간이 걸릴 수 있음)
                timeout = aiohttp.ClientTimeout(total=20)

                async with session.post(self.api_url, json=payload, timeout=timeout) as response:
                    if response.status == 200:
                        data = await response.json()

                        # API 응답: {"win_rate_team_100": 0.6, "win_rate_team_200": 0.4, ...}
                        wr_100 = data.get("win_rate_team_100", 0.0)
                        wr_200 = data.get("win_rate_team_200", 0.0)

                        # 승률이 더 높은 팀 계산
                        if wr_100 >= wr_200:
                            win_team = "블루팀 (Blue)"
                            win_rate = wr_100
                            color = 0x0000FF  # 파란색
                        else:
                            win_team = "레드팀 (Red)"
                            win_rate = wr_200
                            color = 0xFF0000  # 빨간색

                        # 임베드(Embed) 메시지로 예쁘게 출력
                        embed = discord.Embed(
                            title=f"🎮 {riot_id} 승률 분석",
                            description="현재 진행 중인 게임의 GNN 모델 예측 결과입니다.",
                            color=color
                        )
                        embed.add_field(name="예측 승리 팀", value=f"**{win_team}**", inline=True)
                        embed.add_field(name="예측 승률", value=f"**{win_rate * 100:.1f}%**", inline=True)
                        embed.set_footer(text="Powered by LoL Win Prediction Model")

                        await interaction.followup.send(embed=embed)

                    elif response.status == 404:
                        await interaction.followup.send("⚠️ **게임 중이 아닙니다.**\n해당 소환사가 현재 게임을 플레이 중인지 확인해주세요.")
                    elif response.status == 422:
                        await interaction.followup.send("⚠️ **입력 오류**: Riot ID 형식이 올바르지 않거나 존재하지 않는 계정입니다.")
                    else:
                        error_msg = await response.text()
                        await interaction.followup.send(f"⚠️ **서버 오류 ({response.status})**: 관리자에게 문의하세요.")
                        print(f"API Error: {error_msg}")

        except Exception as e:
            await interaction.followup.send(f"🚫 **시스템 에러**: {str(e)}")
            print(f"Bot Logic Error: {e}")


async def setup(bot):
    await bot.add_cog(Prediction(bot))