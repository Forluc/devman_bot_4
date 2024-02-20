import argparse
import os

import redis
from environs import Env


def parse_quiz(file):
    quiz = {}
    for text in file.read().split("\n\n"):
        if not text:
            continue
        header, body = text.split("\n", maxsplit=1)
        if header.startswith("Вопрос"):
            question = " ".join(body.split())
        if header.startswith("Ответ"):
            quiz[question] = " ".join(body.split())
    return quiz


def get_quiz(questions):
    with open(questions, encoding='KOI8-R') as file:
        quiz = parse_quiz(file)

    return quiz


def main():
    env = Env()
    env.read_env()

    parser = argparse.ArgumentParser(description='Скрипт, добавляющий вопросы и ответы в Redis')
    parser.add_argument('-q', '--questions', help='Название файла с вопросами', default=env.str('FILENAME'))
    args = parser.parse_args()
    questions = os.path.join('quiz-question', args.questions)

    redis_connection = redis.Redis(host=env.str('REDIS_HOST'),
                                   port=env.str('REDIS_PORT'),
                                   password=env.str('REDIS_PASSWORD'))

    for question, answer in get_quiz(questions).items():
        redis_connection.set(question, answer)


if __name__ == '__main__':
    main()
