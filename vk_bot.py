import logging
import random

import redis
import vk_api as vk
from environs import Env
from vk_api.keyboard import VkKeyboard
from vk_api.longpoll import VkEventType, VkLongPoll
from vk_api.utils import get_random_id

from quiz import get_quiz

logger = logging.getLogger(__name__)


def handle_new_question_request(event, vk_api, redis_connection, quiz):
    question, answer = random.choice(list(quiz.items()))
    redis_connection.set(event.user_id, answer)

    send_message(event, vk_api, question)


def handle_solution_attempt(event, vk_api, redis_connection):
    if event.text == redis_connection.get(event.user_id):
        send_message(event, vk_api, 'Правильно! Поздравляю! Для следующего вопроса нажми «Новый вопрос»')
    else:
        send_message(event, vk_api, 'Неправильно… Попробуешь ещё раз?')


def handle_surrender(event, vk_api, redis_connection, quiz):
    send_message(event, vk_api, f'Правильный ответ: {redis_connection.get(event.user_id)}')

    question, answer = random.choice(list(quiz.items()))
    redis_connection.set(event.user_id, answer)

    send_message(event, vk_api, question)


def send_message(event, vk_api, message):
    keyboard = VkKeyboard(one_time=True)

    keyboard.add_button('Новый вопрос')
    keyboard.add_button('Сдаться')
    keyboard.add_line()
    keyboard.add_button('Мой счёт')

    vk_api.messages.send(
        user_id=event.user_id,
        message=message,
        random_id=get_random_id(),
        keyboard=keyboard.get_keyboard(),
    )


def main():
    env = Env()
    env.read_env()

    quiz = get_quiz(env.str('QUIZ_NAME', 'example.txt'))
    redis_connection = redis.Redis(host=env.str('REDIS_HOST'), port=env.str('REDIS_PORT'),
                                   password=env.str('REDIS_PASSWORD'), decode_responses=True)

    logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

    vk_session = vk.VkApi(token=env.str('VK_API_KEY'))
    vk_api = vk_session.get_api()
    longpoll = VkLongPoll(vk_session)
    for event in longpoll.listen():
        if event.type == VkEventType.MESSAGE_NEW and event.to_me:
            if event.text == 'Новый вопрос':
                handle_new_question_request(event, vk_api, redis_connection, quiz)
            elif event.text == 'Сдаться':
                handle_surrender(event, vk_api, redis_connection, quiz)
            else:
                handle_solution_attempt(event, vk_api, redis_connection)


if __name__ == "__main__":
    main()
