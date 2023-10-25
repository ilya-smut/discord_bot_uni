import os
import discord
from dotenv import load_dotenv
from discord.ext import commands
import random

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix='!', intents=intents)


@bot.event
async def on_ready():
    print(f'{bot.user.name} has connected to Discord!')


@bot.event
async def on_member_join(member):
    await member.create_dm()
    await member.dm_channel.send(
        f'Hi {member.name}, welcome to my Discord server!'
    )


@bot.command(name='encourage', help='Insults a random member of a channel')
async def nine_nine(ctx):
    guild = ctx.guild
    members = guild.members
    member_list = [member.name for member in members]
    name = random.choice(member_list)

    response = f'{name} is stupid'
    await ctx.send(response)

bot.run(TOKEN)
