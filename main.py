import os


def main():
    questions = os.path.join('quiz-question', '1vs1200.txt')
    with open(questions, encoding='KOI8-R') as file:
        questions = file.read()
    print(questions)


if __name__ == '__main__':
    main()
