import logging
import random

import redis
from environs import Env
from telegram.ext import (CommandHandler, ConversationHandler, Filters,
                          MessageHandler, Updater)

from markups import main_markup, new_answer_markup

logger = logging.getLogger(__name__)

NEW_QUESTION, SOLUTION_ATTEMPT, SURRENDER = range(3)


class QuizBot:
    def __init__(self, tg_bot_api, redis_connection):
        self.question = None
        self.answer = None
        self.redis = redis_connection

        self.updater = Updater(tg_bot_api)
        self.dispatcher = self.updater.dispatcher

        conversation_handler = ConversationHandler(
            entry_points=[CommandHandler('start', self.start)],

            states={
                NEW_QUESTION: [MessageHandler(Filters.regex('^Новый вопрос$'), self.handle_new_question_request)],
                SURRENDER: [MessageHandler(Filters.regex('^Сдаться$'), self.handle_surrender),
                            MessageHandler(Filters.text, self.handle_solution_attempt)],
                SOLUTION_ATTEMPT: [MessageHandler(Filters.text, self.handle_solution_attempt)],
            },

            fallbacks=[]
        )

        self.dispatcher.add_handler(conversation_handler)

    def start(self, update, context):
        context.bot.send_message(chat_id=update.effective_chat.id,
                                 reply_markup=main_markup(),
                                 text='Привет! Я бот для викторин!')

        return NEW_QUESTION

    def handle_new_question_request(self, update, context):
        self.question = random.choice(self.redis.keys())
        self.answer = self.redis.get(self.question)

        context.bot.send_message(chat_id=update.effective_chat.id,
                                 reply_markup=main_markup(),
                                 text=f'{self.question}\n(Ответ должен начинаться с заглавной буквы и оканчиваться точкой, а также разделяться запятыми или союзами по необходимости)')

        return SOLUTION_ATTEMPT

    def handle_solution_attempt(self, update, context):
        if update.message.text == 'Новый вопрос':
            return self.handle_new_question_request(update, context)

        elif update.message.text == self.answer:
            context.bot.send_message(chat_id=update.effective_chat.id,
                                     reply_markup=new_answer_markup(),
                                     text='Правильно! Поздравляю! Для следующего вопроса нажми «Новый вопрос»')
            return NEW_QUESTION

        else:
            context.bot.send_message(chat_id=update.effective_chat.id,
                                     reply_markup=main_markup(),
                                     text='Неправильно… Попробуешь ещё раз?')
            return SURRENDER

    def handle_surrender(self, update, context):
        context.bot.send_message(chat_id=update.effective_chat.id, text=f'Правильный ответ: {self.answer}')

        self.question = random.choice(self.redis.keys())
        self.answer = self.redis.get(self.question)

        context.bot.send_message(chat_id=update.effective_chat.id,
                                 reply_markup=main_markup(),
                                 text=f'{self.question}\n(Ответ должен начинаться с заглавной буквы и оканчиваться точкой, а также разделяться запятыми или союзами по необходимости.)')
        return SOLUTION_ATTEMPT


def main():
    env = Env()
    env.read_env()

    tg_bot_api = env.str('TG_BOT_API')
    redis_connection = redis.Redis(host=env.str('REDIS_HOST'), port=env.str('REDIS_PORT'),
                                   password=env.str('REDIS_PASSWORD'), decode_responses=True)

    logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

    bot = QuizBot(tg_bot_api=tg_bot_api, redis_connection=redis_connection)
    bot.updater.start_polling()
    bot.updater.idle()


if __name__ == '__main__':
    main()
