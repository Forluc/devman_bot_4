import logging
import random

import redis
import vk_api as vk
from environs import Env
from vk_api.keyboard import VkKeyboard
from vk_api.longpoll import VkEventType, VkLongPoll
from vk_api.utils import get_random_id

logger = logging.getLogger(__name__)


class QuizBot:
    def __init__(self, vk_api_key, redis_connection):
        self.question = None
        self.answer = None
        self.redis = redis_connection

        vk_session = vk.VkApi(token=vk_api_key)
        vk_api = vk_session.get_api()
        longpoll = VkLongPoll(vk_session)
        for event in longpoll.listen():
            if event.type == VkEventType.MESSAGE_NEW and event.to_me:
                if event.text == 'Новый вопрос':
                    self.handle_new_question_request(event, vk_api)
                elif event.text == 'Сдаться':
                    self.handle_surrender(event, vk_api)
                else:
                    self.handle_solution_attempt(event, vk_api)

    def handle_new_question_request(self, event, vk_api):
        self.question = random.choice(self.redis.keys())
        self.answer = self.redis.get(self.question)

        self.send_message(event, vk_api, self.question)

    def handle_solution_attempt(self, event, vk_api):
        if event.text == self.answer:
            self.send_message(event, vk_api, 'Правильно! Поздравляю! Для следующего вопроса нажми «Новый вопрос»')
        else:
            self.send_message(event, vk_api, 'Неправильно… Попробуешь ещё раз?')

    def handle_surrender(self, event, vk_api):
        self.send_message(event, vk_api, f'Правильный ответ: {self.answer}')

        self.question = random.choice(self.redis.keys())
        self.answer = self.redis.get(self.question)

        self.send_message(event, vk_api, self.question)

    def send_message(self, event, vk_api, message):
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

    logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

    vk_api_key = env.str('VK_API_KEY')
    redis_connection = redis.Redis(host=env.str('REDIS_HOST'), port=env.str('REDIS_PORT'),
                                   password=env.str('REDIS_PASSWORD'), decode_responses=True)
    QuizBot(vk_api_key, redis_connection)


if __name__ == "__main__":
    main()
