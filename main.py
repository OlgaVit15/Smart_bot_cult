from cProfile import run
import logging
import telegram
from telegram import Update, KeyboardButton
from telegram.ext import Updater, CommandHandler, CallbackContext, MessageHandler, Filters, CallbackQueryHandler, ConversationHandler
from db import getPlaces_create_btn, getPlaces
from location import getLocation


TOKEN = "5720515830:AAE81DWHKRSc9CcOpS68HLEwjFy-zkcU7-E"

MENU, INFORMATION = range(2)


def build_menu(buttons, n_cols, header_buttons=None, footer_buttons=None):
    menu = [buttons[i:i + n_cols] for i in range(0, len(buttons), n_cols)]
    if header_buttons:
        menu.insert(0, [header_buttons])
    if footer_buttons:
        menu.append([footer_buttons])
    return menu


def start(update: Update, context: CallbackContext):
    list_of_btn = [
        KeyboardButton('Расскажи мне об интересных местах!', callback_data='1')
    ]
    reply_markup = telegram.ReplyKeyboardMarkup(
        build_menu(list_of_btn, n_cols=2), resize_keyboard=True)
    update.message.reply_text(
        f'Здравствуйте, {update.effective_user.first_name}! Я - Культ_бот. Чем я могу Вам помочь?',
        reply_markup=reply_markup)

    return MENU


def cancel(update, context):
    user = update.message.from_user
    logging.getLogger(__name__).info(
        "User %s canceled the conversation.", user.first_name)
    update.message.reply_text(
        'Bye! Hope to see you again next time.', reply_markup=telegram.ReplyKeyboardRemove())

    return ConversationHandler.END


def menu(update: Update, context: CallbackContext):
    text = update.message.text
    print(text)
    if (text == "Расскажи мне об интересных местах!") or (text == "Узнать еще"):
        data = getPlaces_create_btn()
        message = 'Выберете место'
        list_of_inner_btn = [f'{row[0]}' for row in data]
        print(list_of_inner_btn)
        reply_inner_markup = telegram.ReplyKeyboardMarkup(build_menu(list_of_inner_btn, n_cols=2),
                                                          one_time_keyboard=True, resize_keyboard=True)
        update.message.reply_text(message, reply_markup=reply_inner_markup)
        return INFORMATION
    else:
        message = 'Возвращайтесь!'
        update.message.reply_text(message, reply_markup=telegram.ReplyKeyboardRemove())
        return ConversationHandler.END


def information(update: Update, context: CallbackContext):
    mess = update.message.text
    print(mess)
    inform = getPlaces(mess)
    print(inform)
    # url = r'D:\ЗАДАНИЯ ИНСТИТУТ\SmartKultBOT\image\\'
    url = '/home/volgavit15/image/'
    photo = open(f'{url}{inform[2]}', 'rb')
    update.message.reply_photo(photo, caption=f"{inform[0]} \n{inform[1]}")
    lon, lat = getLocation(inform[0])
    update.message.reply_location(longitude=lon, latitude=lat)

    list_of_command = [
        KeyboardButton('Узнать еще', callback_data='1'), KeyboardButton('Хватит', callback_data='2')]
    command_markup = telegram.ReplyKeyboardMarkup(build_menu(list_of_command, n_cols=1), resize_keyboard=True)
    update.message.reply_text(
        f'{update.effective_user.first_name}, Вы хотите узнать еще о каком-нибудь месте?',
        reply_markup=command_markup)
    return MENU


def main():
    logging.basicConfig(
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        level=logging.INFO
    )
    
    updater = Updater(TOKEN)

    conv_handler = ConversationHandler(
        entry_points = [CommandHandler('start', start)],    # type: ignore

        states={

            MENU: [MessageHandler(Filters.text, menu)],

            INFORMATION: [MessageHandler(Filters.text, information)],
        },    # type: ignore

        fallbacks=[CommandHandler('cancel', cancel)]
    )

    updater.dispatcher.add_handler(conv_handler)

    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()