import logging
import random

import redis
from environs import Env
from telegram.ext import CommandHandler, Filters, MessageHandler, Updater

from markups import main_markup, new_answer_markup

logger = logging.getLogger(__name__)


class QuizBot:
    def __init__(self, tg_bot_api, redis_connection):
        self.question = None
        self.answer = None
        self.updater = Updater(tg_bot_api)
        self.dispatcher = self.updater.dispatcher
        self.redis = redis_connection

        self.dispatcher.add_handler(CommandHandler('start', self.start))
        self.dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, self.quiz))

    def start(self, update, context):
        context.bot.send_message(chat_id=update.effective_chat.id,
                                 reply_markup=main_markup(),
                                 text='Привет! Я бот для викторин!')

    def quiz(self, update, context):
        if update.message.text == 'Новый вопрос':
            self.question = random.choice(self.redis.keys()).decode('utf8')
            self.answer = self.redis.get(self.question).decode('utf8')
            context.bot.send_message(chat_id=update.effective_chat.id,
                                     reply_markup=main_markup(),
                                     text=f'{self.question}\n(Ответ должен начинаться с заглавной буквы и оканчиваться точкой, а также разделяться запятыми или союзами по необходимости.)')

        elif update.message.text == self.answer:
            context.bot.send_message(chat_id=update.effective_chat.id,
                                     reply_markup=new_answer_markup(),
                                     text='Правильно! Поздравляю! Для следующего вопроса нажми «Новый вопрос»')
        else:
            context.bot.send_message(chat_id=update.effective_chat.id,
                                     reply_markup=main_markup(),
                                     text='Неправильно… Попробуй ещё раз')


def main():
    env = Env()
    env.read_env()

    tg_bot_api = env.str('TG_BOT_API')
    redis_connection = redis.Redis(host=env.str('REDIS_HOST'), port=env.str('REDIS_PORT'),
                                   password=env.str('REDIS_PASSWORD'))

    logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

    bot = QuizBot(tg_bot_api=tg_bot_api, redis_connection=redis_connection)
    bot.updater.start_polling()
    bot.updater.idle()


if __name__ == '__main__':
    main()
