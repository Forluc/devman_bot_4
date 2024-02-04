import logging
from random import choice

from telegram import Update, ReplyKeyboardMarkup, ReplyKeyboardRemove
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext
from environs import Env
from quiz import get_quiz

logger = logging.getLogger(__name__)


def start(update: Update, context: CallbackContext):
    custom_keyboard = [['Новый вопрос', 'Сдаться'],
                       ['Мой счёт']]
    reply_markup = ReplyKeyboardMarkup(custom_keyboard)
    context.bot.send_message(chat_id=update.effective_chat.id,
                             reply_markup=reply_markup,
                             text='Привет! Я бот для викторин!')


def quiz(update: Update, context: CallbackContext):
    reply_markup = ReplyKeyboardRemove()
    if update.message.text == 'Новый вопрос':
        question, answer = choice(list(get_quiz().items()))
        context.bot.send_message(chat_id=update.effective_chat.id, text=question, reply_markup=reply_markup)


def main():
    logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

    env = Env()
    env.read_env()

    updater = Updater(env.str('TG_BOT_API'))

    dispatcher = updater.dispatcher
    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, quiz))

    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()
