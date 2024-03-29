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

`TG_BOT_API` = Присвоить `API-токен` телеграм
бота([инструкция](https://robochat.io/docs/kak-sozdat-chat-bota-v-telegram/))

`VK_API_KEY` = Присвоить `API-ключ` группы
вконтакте. ([Инструкция](https://pechenek.net/social-networks/vk/api-vk-poluchaem-klyuch-dostupa-token-gruppy/))

`QUIZ_NAME` = Присвоить `название файла`, вопросы которого, будут отправляться пользователям(по умолчанию `example.txt`)

После заполнения данных, можно прочитать файл `.env` можно увидеть примерно следующее:

```bash
$ cat .env
TG_BOT_API='11111111:tgbotapiexample'
VK_API_KEY='vkapikeyexample'
REDIS_HOST='your_address'
REDIS_PORT='your_port'
REDIS_PASSWORD='your_password'
QUIZ_NAME='example.txt'
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

### Цель проекта

Скрипт написан в образовательных целях на онлайн-курсе [Devman](https://dvmn.org)
