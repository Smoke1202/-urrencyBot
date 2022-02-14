import telebot
from Utils import ConvertionException, CryptoConverter
from config import TOKEN, CryptoCurr, Curr, icons


bot = telebot.TeleBot(TOKEN)


@bot.message_handler(commands=['start', 'help'])
def activate_test(message: telebot.types.Message):
    bot.reply_to(message, f'Здравствуй {message.chat.username}\nЯ бот-конвертер, я умею конвертировать физическую валюту и криптовалюту.'
    f'Для списка популяртых криптовалют введите команду /cryptocurrency, а для списка физической валюты введите /currency.\n'
    f'Чтобы конвертировать валюту напишите её в следующем формате:\n'
    f'      <имя валюты> \n'
    f'      <в какую валюту перевести>  \n'
    f'      <количество переводимой валюты> \n'
    f'Например: USD RUB 100. Не обязательно с заглавных🤗')


@bot.message_handler(commands=['currency'])
def values(message: telebot.types.Message):
    text = '\n'
    for key in Curr.values():
        text = '\n'.join((text, key,))
    bot.reply_to(message, text)


@bot.message_handler(commands=['cryptocurrency'])
def values(message: telebot.types.Message):
    text = '\n'
    for key in CryptoCurr.values():
        text = '\n'.join((text, key, ))
    bot.reply_to(message, text)


@bot.message_handler(content_types=['text', ])
def convert(message: telebot.types.Message):
    try:
        values = message.text.split(' ')

        if len(values) != 3:
            raise ConvertionException('Неверный ввод, пожалуйста, укажите 2 валюты и сумму, которую вы хотите конвертировать')

        quote, base, amount = values
        total_base = CryptoConverter.convert(*values)
        if float(amount) < 0:
            raise ConvertionException(f'')

    except Exception as e:
        bot.reply_to(message, f'Извините, но мы не поддерживаем эти валюты\n{e}')
    else:
        text = "{:f}".format(total_base) + f'  {icons.get(base.upper())}'

        bot.send_message(message.chat.id, text)




bot.polling()
