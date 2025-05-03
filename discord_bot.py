import os, threading, asyncio
import discord
from embedder import query_similar
import openai
import config

intents = discord.Intents.default()
intents.message_content = True
bot = discord.Bot(intents=intents)

openai.api_key = config.OPENAI_API_KEY

@bot.event
async def on_ready():
    print(f"Discord Bot logged in as {bot.user}")

@bot.event
async def on_message(message):
    if message.author.bot: return
    user_msg = message.content
    # Tìm context
    docs = query_similar(user_msg)
    system = [{'role':'system','content':'Bạn là AI Discord.'}]
    for d in docs: system.append({'role':'system','content': d})
    system.append({'role':'user','content': user_msg})
    resp = openai.ChatCompletion.create(model='gpt-4o-mini', messages=system)
    await message.reply(resp.choices[0].message.content)


def run_discord():
    bot.run(config.DISCORD_TOKEN)

# Chạy bot trong thread riêng
threading.Thread(target=run_discord, daemon=True).start()
