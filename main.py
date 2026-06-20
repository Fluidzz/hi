import discord
from discord.ext import commands
import os
import asyncio  # For potential delays

intents = discord.Intents.default()
intents.members = True

bot = commands.Bot(command_prefix='!', intents=intents)

@bot.event
async def on_ready():
    print(f'Bot logged in as {bot.user}')

@bot.command()
@commands.has_permissions(manage_nicknames=True)
async def resetnicks(ctx):
    await ctx.send("🔄 Resetting all nicknames... This may take time on big servers.")
    count = 0
    failed = 0
    for member in ctx.guild.members:
        if not member.bot and member.nick is not None:
            try:
                await member.edit(nick=None, reason="Server recovery after nuke")
                count += 1
                await asyncio.sleep(0.5)  # Avoid rate limits
            except discord.Forbidden:
                failed += 1
            except Exception as e:
                print(f"Error with {member}: {e}")
                failed += 1
    await ctx.send(f"✅ Finished! Reset **{count}** nicknames. Failed: **{failed}**.")

# Keep-alive (important for Replit)
from flask import Flask
from threading import Thread

app = Flask('')

@app.route('/')
def home():
    return "Bot is alive!"

def run():
    app.run(host='0.0.0.0', port=8080)

def keep_alive():
    t = Thread(target=run)
    t.start()

keep_alive()

bot.run(os.getenv('TOKEN'))