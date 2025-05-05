# discord-bot/bot.py

import os
import discord
from discord.ext import commands
import openai

# —————— Setup OpenAI ——————
openai.api_key = os.getenv("OPENAI_API_KEY")

# —————— Setup Discord Bot với intents ——————
intents = discord.Intents.default()
intents.message_content = True

class AIClient(commands.Bot):
    def __init__(self):
        super().__init__(command_prefix="!", intents=intents)

    async def setup_hook(self):
        # load all cogs asynchronously
        for filename in os.listdir("./commands"):
            if filename.endswith(".py"):
                await self.load_extension(f"commands.{filename[:-3]}")
bot = AIClient()


@bot.event
async def on_ready():
    print(f"Logged in as {bot.user} (ID: {bot.user.id})")

# —————— Chat tự nhiên: bắt mọi message không phải bot ——————
@bot.event
async def on_message(message):
    # bỏ qua chính bot
    if message.author.bot:
        return

    # nếu bạn vẫn muốn hỗ trợ prefix commands,
    # gọi tiếp process_commands trước khi chat AI
    await bot.process_commands(message)

    # giờ handle free-form chat:
    prompt = message.content

    # Gửi prompt đến OpenAI ChatCompletion
    try:
        resp = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user",    "content": prompt}
            ],
            temperature=0.7,
        )
        answer = resp.choices[0].message.content.strip()
        await message.channel.send(answer)
    except Exception as e:
        await message.channel.send("⚠️ Có lỗi khi gọi OpenAI:\n" + str(e))

# —————— Chạy bot ——————
DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")
if __name__ == "__main__":
    bot.run(DISCORD_TOKEN)
