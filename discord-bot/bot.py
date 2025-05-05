# discord-bot/bot.py

import os, discord
from discord.ext import commands
import openai

openai.api_key = os.getenv("OPENAI_API_KEY")

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

        # sau khi load xong, có thể khởi tạo thread background nếu cần

# khởi tạo bot
bot = AIClient()

@bot.event
async def on_ready():
    print(f"Logged in as {bot.user} (ID: {bot.user.id})")

@bot.event
async def on_message(message):
    if message.author.bot:
        return
    await bot.process_commands(message)
    # free-form chat...
    resp = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role":"system","content":"You are a helpful assistant."},
            {"role":"user","content":message.content}
        ],
        temperature=0.7
    )
    await message.channel.send(resp.choices[0].message.content.strip())

# ping command có thể giữ nguyên trong commands/ping.py

if __name__ == "__main__":
    bot.run(os.getenv("DISCORD_TOKEN"))

