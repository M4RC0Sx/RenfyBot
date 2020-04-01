# RenfyBot
Telegram bot made with Python Telegram API that aims to make it easy to check timetables of trains from RENFE service in Madrid.

## Requeriments
* Python3
* Python3 - python-telegram-bot
* Python3 - logging
* Python3 - json
* Python3 - os
* Python3 - sys
* Python3 - requests
* Python3 - datetime

## Instructions
1. Clone the repository.
2. Edit the file bot_token.py and change the constant **BOT_TOKEN** according to your Telegram Bot. (You must create it and get this params via BotFather).
3. Run the bot on your server, raspberry... A good idea is to create a screen for it and attach it there.
4. **IMPORTANT: All files must be in the same directory. A file renfy_bot.log will be created there.**


## Commands
* **/help -** General help command.
* **/credits -** Credits to the bot author.
* **/stations -** List current available stations (according to stations.json file).
* **/time \<origin\> \<target\> -** See next trains between given origin and target stations.


## Additional Notes
The bot is currently working and active 24/7. In case you want to use it or check its functionallity, you can start a conversation with in Telegram using the following link: **http://t.me/renfy_bot**

## Some Screenshots
<img src="https://i.imgur.com/4KuWYht.png" title="Screenshot#1 - General Screenshot">