import telebot
from config import TOKEN, keys
from extensions import ConvertionException, CryptoConverter


bot = telebot.TeleBot(TOKEN)


@bot.message_handler(commands=['start'])
def start(message: telebot.types.Message):
    text = f'Привет, {message.chat.first_name}!\n\
Я — бот-конвертер валют и я могу:\n\
Показать список доступных валют по команде: /values\n\
Провести конвертацию валюты:\n\
Пример запроса: доллар евро 1\n\
Пример ответа: Цена за 1 доллар в евро - 0.97\n\
Подробнее по шагам конвертации: /help'
    bot.reply_to(message, text)


@bot.message_handler(commands=['help'])
def help_(message: telebot.types.Message):
    text = f'Привет, {message.chat.first_name}!\n\
Если у Вас возникли затруднения, тогда:\n\
Для конвертации валюты, введите через пробел:\n\
1. <имя переводимой валюты>\n\
2. <в какую валюту перевести>\n\
3. <количество переводимой валюты>\n\
Пример запроса: доллар евро 1\n\
Пример ответа: Цена за 1 доллар в евро - 0.97\n\
Показать список доступных валют: /values\n\
Вернуть Вас в начало: /start'
    bot.reply_to(message, text)


@bot.message_handler(commands=['values'])
def values(message: telebot.types.Message):
    text = 'Доступные валюты:'
    for key in keys.keys():
        text = '\n'.join((text, key, ))
    bot.reply_to(message, text)


@bot.message_handler(content_types=['text', ])
def convert(message: telebot.types.Message):
    try:
        check = message.text.split(' ')

        if len(check) != 3:
            raise ConvertionException('Введите команду или 3 параметра')

        quote, base, amount = check
        total_base = CryptoConverter.get_price(quote, base, amount)
    except ConvertionException as e:
        bot.reply_to(message, f'Ошибка пользователя.\n{e}')
    except Exception as e:
        bot.reply_to(message, f'Что-то пошло не так с {e}')
    else:
        text = f'Цена за {amount} {quote} в {base} - {total_base}'
        bot.send_message(message.chat.id, text)


@bot.message_handler(content_types=['voice'])
def repeat(message: telebot.types.Message):
    bot.send_message(message.chat.id, f"Привет, {message.chat.first_name}! Рад слышать!")


@bot.message_handler(content_types=['sticker'])
def say_lmao(message: telebot.types.Message):
    bot.reply_to(message, 'Ахах, умора!')


bot.polling()
