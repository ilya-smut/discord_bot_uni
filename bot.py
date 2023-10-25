import os
import discord
from dotenv import load_dotenv
from discord.ext import commands
import random

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
W_CHANNEL = os.getenv('WELCOME_CHANNEL')

intents = discord.Intents.default()
intents.members = True
intents.message_content = True

bot = commands.Bot(command_prefix='!', intents=intents)


@bot.event
async def on_ready():
    print(f'{bot.user.name} has connected to Discord!')


@bot.event
async def on_member_join(member):

    welcome_channel = bot.get_channel(int(W_CHANNEL))

    if welcome_channel:
        welcome_message = (
            f'Hi @{member.name}, welcome to ASS (Advanced Security Society)! \n\n'
            'We are trying here build a supporting environment '
            'for like-minded people on the course, who are really interested '
            'in the course. We discuss stuff, ask questions, help each other, etc. '
            '\n\nThere are some pretty simple rules: use your **real name** as a server nickname, '
            'do not insult or bully people, and stick to the server purpose. If you have '
            'some questions regarding studying, ask them in #question-channel :)\n\n'
            'Please, feel free to say "Hi!" in #speak-here'

        )
        await welcome_channel.send(welcome_message)


@bot.command(name='encourage', help='Says good stuff about a random member of a server')
async def nine_nine(ctx):
    guild = ctx.guild
    members = guild.members
    member_list = [member.name for member in members]
    word_list = [
        'clever', 'smart', 'intelligent', 'bright', 'sharp', 'astute', 'ingenious', 'resourceful', 'knowledgeable',
        'quick-witted', 'shrewd', 'brainy', 'crafty', 'cunning', 'wise', 'savvy', 'sharp-witted', 'apt', 'adroit',
        'perceptive'
    ]
    name = random.choice(member_list)
    word = random.choice(word_list)

    response = f'{name} is {word}'
    await ctx.send(response)

bot.run(TOKEN)
