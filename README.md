# Квиз-Боты в телеграм и ВК

Боты отправляют вопросы на которые нужно ответить. Берут данные из своей БД [Redis](https://app.redislabs.com/). Через
скрипт можно добавлять вопросы в БД.

- [Ознакомиться](https://t.me/dvmn_quizzz_bot) с телеграм ботом
- [Ознакомиться](https://vk.com/club224635074) с ботом Вконтакте

## Окружение

### Требования к установке

Python3 должен быть уже установлен. Затем используйте pip (или pip3, есть конфликт с Python2) для установки
зависимостей:

```bash
pip install -r requirements.txt
```

### Подготовка БД [Redis](https://app.redislabs.com/)

1) Зарегистрироваться на [сайте](https://app.redislabs.com/)
2) Получить адрес базы данных вида: redis-13965.f18.us-east-4-9.wc1.cloud.redislabs.com, его порт вида: 16635 и его
   пароль.
3) Создать файл `.env` и добавить в него данные:

```
REDIS_HOST='your_address'
REDIS_PORT='your_port'
REDIS_PASSWORD='your_password'
```

### Добавление остальных чувствительных данных в `.env`

Обязательные к заполнению переменные:

`TG_BOT_API` = Присвоить `API-токен` телеграм
бота([инструкция](https://robochat.io/docs/kak-sozdat-chat-bota-v-telegram/))

`VK_API_KEY` = Присвоить `API-ключ` группы
вконтакте. ([Инструкция](https://pechenek.net/social-networks/vk/api-vk-poluchaem-klyuch-dostupa-token-gruppy/))

Необязательные к заполнению переменные:

`FILENAME` = Присвоить `название файла`, вопросы которого, необходимо добавить в [Redis](https://app.redislabs.com/)

После заполнения данных, можно прочитать файл `.env` можно увидеть примерно следующее:

```bash
$ cat .env
TG_BOT_API='11111111:tgbotapiexample'
VK_API_KEY='vkapikeyexample'
REDIS_HOST='your_address'
REDIS_PORT='your_port'
REDIS_PASSWORD='your_password'
FILENAME='filename.txt'
```

### Запуск ботов

Запуск бота Вконтакте на Linux(Python 3) или Windows:

```bash
$ python vk_bot.py
```

Запуск бота Телеграм на Linux(Python 3) или Windows:

```bash
$ python tg_bot.py
```

### Добавление вопросов в БД [Redis](https://app.redislabs.com/)

- Добавить файл в папку quiz-question и заполнить нужными вопросами и ответами. Файл закодирован `KOI8-R`(Пример
  заполнения файла есть в папке, название файла `example.txt`)
- Обязательны к заполнению в `.env` данные от Redis(host, port, password) и название файла

После заполнения данных, можно прочитать файл `.env` можно увидеть примерно следующее:

```bash
$ cat .env
REDIS_HOST='your_address'
REDIS_PORT='your_port'
REDIS_PASSWORD='your_password'
FILENAME='filename.txt'
```

Запуск скрипта без использования argparse:

```bash
$ python populating_db_redis.py
```

Запуск скрипта с использованием argparse:

```bash
$ python populating_db_redis.py --questions example.txt
```

Какие вопросы добавлены в БД можно посмотреть с помощью [RedisInsight](https://app.redislabs.com/)

### Цель проекта

Скрипт написан в образовательных целях на онлайн-курсе [Devman](https://dvmn.org)
