import sys
import logging
from telegram.ext import (Updater, CommandHandler)
import telegram

import utils
import renfe_scrapper as rs


# Logger initialization.
logging.basicConfig(filename='renfy_bot.log', format=utils.BOT_PREFIX + "%(asctime)s - %(levelname)s - %(message)s",
                    level=logging.INFO)
logger = logging.getLogger(__name__)
logger.addHandler(logging.StreamHandler(sys.stdout))

# Station data global variable.
station_data = {}


def get_timetable(update, context):

    # Check arguments.
    args = context.args
    if args is None or len(args) < 2:
        update.message.reply_text(utils.PREFIX_ERROR + "Incorrect usage! <b>Correct usage:</b> <i>/time [origin] [target]</i>.", parse_mode=telegram.ParseMode.HTML)
        return

    # Check if there are registered stations.
    if len(station_data) <= 0 or station_data is None:
        logger.warning("Could not find train stations data.")
        return

    # Parse origin and target arguments.
    origin = station_data[args[0]]
    target = station_data[args[1]]
    if origin is None or target is None:
        update.message.reply_text(utils.PREFIX_ERROR + "There is an error on your origin and/or target. Check them.", parse_mode=telegram.ParseMode.HTML)
        return

    # Get RENFE data according to given origin and target.
    renfe_data = rs.get_renfe_data(origin, target)
    if len(renfe_data) > 0:
        update.message.reply_text(utils.PREFIX_INFO + "Next trains from <i>{}</i> to <i>{}</i>:".format(args[0], args[1]), parse_mode=telegram.ParseMode.HTML)
        for i in renfe_data:
            if i['accesible']:
                update.message.reply_text("<b>🚂 Line:</b> {}\n<b>🕒 Departure Time:</b> {}\n<b>🕥 Arrival Time:</b> {}\n<b>⏳ Duration:</b> {}\n<b>👨‍🦽 Accessible: ✅</b> ".format(i['linea'], i['horaSalida'], i['horaLlegada'], i['duracion']), parse_mode=telegram.ParseMode.HTML)
            else:
                update.message.reply_text("<b>🚂 Line:</b> {}\n<b>🕒 Departure Time:</b> {}\n<b>🕥 Arrival Time:</b> {}\n<b>⏳ Duration:</b> {}\n<b>👨‍🦽 Accessible: ❌</b> ".format(i['linea'], i['horaSalida'], i['horaLlegada'], i['duracion']), parse_mode=telegram.ParseMode.HTML)
    else:
        update.message.reply_text(utils.PREFIX_INFO + "There are no next trains available from <i>{}</i> to <i>{}</i>. Sorry.".format(args[0], args[1]), parse_mode=telegram.ParseMode.HTML)
        update.message.reply_text(utils.PREFIX_INFO + "Maybe it is a temporary error getting data from RENFE.".format(args[0], args[1]), parse_mode=telegram.ParseMode.HTML)

    logger.info("Function get_timetable has been executed. [ChatID: {} - User: {}]".format(update.message.chat_id, update.message.from_user.username))


def get_stations(update, context):

    # Print loaded stations from JSON.
    if len(station_data) > 0:
        update.message.reply_text(utils.PREFIX_INFO + "Current available stations for origin or target:", parse_mode=telegram.ParseMode.HTML)

        txt = ""
        for i in station_data.keys():
            txt += (str(i) + "\n")
        update.message.reply_text(txt)

    else:
        update.message.reply_text(utils.PREFIX_ERROR + "There are no stations available yet.", parse_mode=telegram.ParseMode.HTML)

    logger.info("Function get_stations has been executed. [ChatID: {} - User: {}]".format(update.message.chat_id, update.message.from_user.username))


def command_help(update, context):

    update.message.reply_text(utils.PREFIX_INFO + "<b>/help</b> - General bot information and commands.", parse_mode=telegram.ParseMode.HTML)
    update.message.reply_text(utils.PREFIX_INFO + "<b>/credits</b> - Bot author credits.", parse_mode=telegram.ParseMode.HTML)
    update.message.reply_text(utils.PREFIX_INFO + "<b>/stations</b> - List of available stations.", parse_mode=telegram.ParseMode.HTML)
    update.message.reply_text(utils.PREFIX_INFO + "<b>/time</b> - Check next trains between given origin and target as arguments.", parse_mode=telegram.ParseMode.HTML)

    logger.info("Function command_help has been executed. [ChatID: {} - User: {}]".format(update.message.chat_id, update.message.from_user.username))


def command_credits(update, context):

    update.message.reply_text("<b>RenfyBot - Developed by: M4RC0Sx</b>", parse_mode=telegram.ParseMode.HTML)
    update.message.reply_text("Thank you for using it! Remember to <i>follow me on GitHub</i>:", parse_mode=telegram.ParseMode.HTML)
    update.message.reply_text('<b><a href="https://github.com/M4RC0Sx">My Awesome GitHub</a></b>', parse_mode=telegram.ParseMode.HTML)

    logger.info("Function command_credits has been executed. [ChatID: {} - User: {}]".format(update.message.chat_id, update.message.from_user.username))


def main():

    # Declare bot updater and command dispatcher.
    updater = Updater(utils.BOT_TOKEN, use_context=True)
    dp = updater.dispatcher
    dp.add_handler(CommandHandler('stations', get_stations))
    dp.add_handler(CommandHandler('time', get_timetable))
    dp.add_handler(CommandHandler('help', command_help))
    dp.add_handler(CommandHandler('credits', command_credits))

    # Load stations from JSON file.
    global station_data
    station_data = utils.load_stations()
    if station_data is None:
        logger.error("Could not open train stations data file.")
        return

    # Start the Telegram bot.
    updater.start_polling()

    logger.info("RenfyBot has been correctly started.")

    # Run until SIGINT.
    updater.idle()


if __name__ == '__main__':
    main()
