# **Discord University Bot**

The *Discord University Bot* is a feature-rich Discord bot designed by Cyber Security student at De Montfort University to enhance and simplify student cohort server management experience. With a wide range of useful commands, the bot aims to assist admins and provide users with fun and utility commands.

## **Features**

### **Welcoming New Members**

The bot sends a custom welcome message to new members joining the server. You can modify the welcome message in the `bot.py` file.

### **Encouragement Command**

The `encourage` command selects a random user from the server and compliments them with a word from a predefined list.

### **Complaints System**

Users can file complaints using the `cmp` command. The complaint is then saved with a unique key. All complaints can be viewed using the `cmp-all` command, or a specific complaint can be retrieved using its unique key with the `cmp-get` command.

### **Word Definitions**

The `def` command fetches definitions for a given word using an API, providing a useful tool for quick look-ups without leaving Discord.

### **Encoding and Decoding Utilities**

The bot provides commands for base64 and URL encoding and decoding, offering a handy utility for developers.

## **Setup**

To set up the bot, you need to specify the bot token, welcome channel, and the core path in a `.env` file.

## **Usage**

To use the bot, run `bot.run(TOKEN)` at the bottom of the `bot.py` file.

## **Dependencies**

The bot uses the following dependencies which need to be installed:

- `os`
- `discord`
- `dotenv`
- `commands`
- `random`

## **Contributing**

Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

## **License**

[MIT](https://choosealicense.com/licenses/mit/)
