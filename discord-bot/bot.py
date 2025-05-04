import os
import discord
from discord.ext import commands

# prefix hoặc dùng slash, tùy bạn
bot = commands.Bot(command_prefix="!")

# load tất cả các command modules trong thư mục commands/
for filename in os.listdir("./commands"):
    if filename.endswith(".py"):
        bot.load_extension(f"commands.{filename[:-3]}")

@bot.event
async def on_ready():
    print(f"Logged in as {bot.user} (ID: {bot.user.id})")

# Lấy token từ biến môi trường
DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")

if __name__ == "__main__":
    bot.run(DISCORD_TOKEN)
