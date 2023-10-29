import os
import discord
from dotenv import load_dotenv
from discord.ext import commands
import random
import complaints

# Getting parameters from .env file
load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
W_CHANNEL = os.getenv('WELCOME_CHANNEL')
core_path = os.getenv('CORE_PATH')

# Specifying permissions bot has. Default + members + messages
intents = discord.Intents.default()
intents.members = True
intents.message_content = True

# Specifying the symbol bot uses for commands
bot = commands.Bot(command_prefix='!', intents=intents)


# The message will be printed to the console if bot has successfully connected to discord
@bot.event
async def on_ready():
    print(f'{bot.user.name} has connected to Discord!')


# The welcome message printed by the bot when a new user joins. You can change the content of welcome_message to make
# your own custom message
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


# Fun command that chooses a random user from members and calls them a random good word from the word_list
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


# The following function is used to add a complaint to a server's complaints file
# It checks if the server's complaints directory exists and if not - creates one
# Then it takes user's nickname and uses it as a key for the complaints' dictionary
# If user id is already a key in dictionary, it adds 1 to it.
# So if user adds a lot of complaints, their keys would look like 'userid', 'userid1', 'userid2', ...
@bot.command(name='cmp', help='Files a complaint to the bot')
async def add_complaint(ctx, *args):
    guild = ctx.guild
    author = ctx.message.author.name
    message = ' '.join(args)
    dir_path = core_path + str(guild)
    file_path = dir_path + "/complaints.txt"
    if not os.path.isdir(dir_path):
        os.mkdir(core_path + str(guild))

    db = complaints.ComplaintsDb()
    await db.load(file_path)

    key = str(author)
    start_length = len(key)
    existent_keys = db.get_keys()
    while key in existent_keys:
        if len(key) == start_length:
            key = key + '1'
        else:
            extra = int(key[start_length:])
            extra += 1
            key = key[:start_length] + str(extra)

    db.add_complaint(key, message)
    db.save()
    await ctx.send('Complaint added with key = ' + str(key) + '; Text = ' + message)


# Printing all complaints to the channel where command was called
@bot.command(name='cmp-all', help='Prints all complaints')
async def get_complaints(ctx):
    guild = ctx.guild
    dir_path = core_path + str(guild)
    file_path = dir_path + "/complaints.txt"
    if not os.path.isdir(dir_path):
        os.mkdir(core_path + str(guild))

    db = complaints.ComplaintsDb()
    await db.load(file_path)

    bot_response = '**Here is the list of complaints**: \n\n' + '\n\n'.join(db.get_all_complaints())

    await ctx.send(bot_response)


# Printing a single complaint to the channel where the command was called. User needs to specify id
# after !cmp-get. Example: !cmp-get {complaint_id}
@bot.command(name='cmp-get', help='Gets a complaint by complaint-id')
async def get_complaint(ctx, arg1):
    guild = ctx.guild
    dir_path = core_path + str(guild)
    file_path = dir_path + "/complaints.txt"
    if not os.path.isdir(dir_path):
        os.mkdir(core_path + str(guild))
    db = complaints.ComplaintsDb()
    await db.load(file_path)

    if arg1 in db.get_keys():
        await ctx.send(db.get_complaint(arg1))
    else:
        await ctx.send('No complaint found')

# Running the bot
bot.run(TOKEN)
