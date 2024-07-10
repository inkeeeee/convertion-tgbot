import telebot

from config import keys, token
from extensions import ConvertionException, Converter

bot = telebot.TeleBot(token)


@bot.message_handler(commands=['start'])
def handle_start_help(message: telebot.types.Message):
    bot.send_message(message.chat.id,
                     f'{message.chat.first_name}, здравствуйте. Чтобы посмотреть инструкцию к боту, напишите /help')


@bot.message_handler(commands=['help'])
def handle_help(message: telebot.types.Message):
    bot.send_message(message.chat.id,
                     f'1. Чтобы узнать стоимость одной валюты в другой, нужно написать следущее: <название конвертируемой валюты> <название валюты, в которую желаете конвертироать> <кол-во валюты>\nПример команды: доллар рубль 8\n2. Напишите /values, чтобы узнать доступные валюты')


@bot.message_handler(commands=['values'])
def values(message: telebot.types.Message):
    text = 'Доступные валюты:'
    for el in keys:
        text += f'\n{el}'

    bot.send_message(message.chat.id, text)


@bot.message_handler(content_types=['text'])
def convert(message: telebot.types.Message):
    try:
        data = message.text.lower().split()
        if len(data) != 3:
            raise ConvertionException('Неверное кол-во параметров')

        quote, base, amount = message.text.lower().split()
        total = Converter.get_price(quote, base, amount)
        iso_quote, iso_base = keys[quote], keys[base]
        text = f'Стоимость {amount} {iso_quote} в {iso_base} - {total}'


    except ConvertionException as e:
        bot.send_message(message.chat.id, f'Ошибка пользователя\n{e}')

    except Exception:
        bot.send_message(message.chat.id, 'Не удалось обработать запрос')

    else:
        bot.send_message(message.chat.id, text)


bot.polling(non_stop=True)
