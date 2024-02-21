import logging
import random

import redis
from environs import Env
from telegram import ReplyKeyboardMarkup
from telegram.ext import (CommandHandler, ConversationHandler, Filters,
                          MessageHandler, Updater)

from quiz import get_quiz

logger = logging.getLogger(__name__)

NEW_QUESTION, SOLUTION_ATTEMPT, SURRENDER = range(3)


def start(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id,
                             reply_markup=get_markup(),
                             text='Привет! Я бот для викторин!')

    return NEW_QUESTION


def handle_new_question_request(update, context):
    question, answer = random.choice(list(get_quiz(context.bot_data['quiz']).items()))
    context.bot_data['redis'].set(update.effective_chat.id, answer)

    context.bot.send_message(chat_id=update.effective_chat.id,
                             reply_markup=get_markup(),
                             text=question)

    return SOLUTION_ATTEMPT


def handle_solution_attempt(update, context):
    if update.message.text == 'Новый вопрос':
        return handle_new_question_request(update, context)

    elif update.message.text == context.bot_data['redis'].get(update.effective_chat.id):
        context.bot.send_message(chat_id=update.effective_chat.id,
                                 reply_markup=get_markup(),
                                 text='Правильно! Поздравляю! Для следующего вопроса нажми «Новый вопрос»')
        return NEW_QUESTION

    else:
        context.bot.send_message(chat_id=update.effective_chat.id,
                                 reply_markup=get_markup(),
                                 text='Неправильно… Попробуешь ещё раз?')
        return SURRENDER


def handle_surrender(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id,
                             text=f'Правильный ответ: {context.bot_data["redis"].get(update.effective_chat.id)}')

    question, answer = random.choice(list(get_quiz(context.bot_data['quiz']).items()))
    context.bot_data['redis'].set(update.effective_chat.id, answer)

    context.bot.send_message(chat_id=update.effective_chat.id,
                             reply_markup=get_markup(),
                             text=question)
    return SOLUTION_ATTEMPT


def get_markup():
    return ReplyKeyboardMarkup([['Новый вопрос', 'Сдаться'], ['Мой счёт']])


def main():
    env = Env()
    env.read_env()

    quiz = env.str('QUIZ_NAME', 'example.txt')
    redis_connection = redis.Redis(host=env.str('REDIS_HOST'), port=env.str('REDIS_PORT'),
                                   password=env.str('REDIS_PASSWORD'), decode_responses=True)

    logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

    updater = Updater(env.str('TG_BOT_API'))
    dispatcher = updater.dispatcher
    dispatcher.bot_data['redis'] = redis_connection
    dispatcher.bot_data['quiz'] = quiz
    dispatcher.add_handler(
        ConversationHandler(
            entry_points=[CommandHandler('start', start)],

            states={
                NEW_QUESTION: [MessageHandler(Filters.regex('^Новый вопрос$'), handle_new_question_request)],
                SURRENDER: [MessageHandler(Filters.regex('^Сдаться$'), handle_surrender),
                            MessageHandler(Filters.text, handle_solution_attempt)],
                SOLUTION_ATTEMPT: [MessageHandler(Filters.text, handle_solution_attempt)],
            },

            fallbacks=[]
        )
    )

    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()
