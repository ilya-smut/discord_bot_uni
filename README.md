A simple discord bot for a student discord chat

It is built using discord.py
https://github.com/Rapptz/discord.py

Currently comes with a simple set of functions:
1) Greet new members with a custom message in the welcome_channel (welcome channel's id should be specified in .env
2) Fun !encourage command that chooses a random user from the server and gives them a random compliment
3) "Complaints" set of command which allows users to input complaints in the bot. This set of complaints than can be used by a student rep to escalate it to programme leaders
4) Bot can also give you a definition of the English word using !def {word} command

Separate file for complaints is created for each discord server. You need to specify the path for the directory that will store all complaints in .env

You can add a complaint using !cmp {message} command
You can list all complaints using !cmp-all command
You can print a single complaint using its id with !cmp-get {id} command

.env file specifies following parameters:
DISCORD_TOKEN - your discord token
WELCOME_CHANNEL - welcome-channel's id for your server
CORE_PATH - the path to the directory that stores complaints

