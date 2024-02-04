import os


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


def main():
    questions = os.path.join('quiz-question', '3f15.txt')
    with open(questions, encoding='KOI8-R') as file:
        quiz = parse_quiz(file)


if __name__ == '__main__':
    main()
