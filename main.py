import telebot
import requests

def check_field(text:str, key, msht:bool) -> str:
      msh = ''

      if msht:
            msh = '```'

      if ( key is not None):
            return f'{text}{msh}\n{str(key)}\n{msh}\n'
      else:
            return ''


bot = telebot.TeleBot("7045715363:AAFG6sYgU_1SrFHVQjLA5jh3rdZ0cThcMwg")

@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
	bot.reply_to(message, "Тестовое задание для Venator")

@bot.message_handler(func=lambda message: True)
def echo_all(message):
    tel_number = message.text
    htmlweb_url = f'https://htmlweb.ru/geo/api.php?json&telcod=%7b{tel_number}%7d&api_key=d9b88e7c252c3361e52a351bfc09037d'

    htmlweb_request = requests.get(htmlweb_url)

    response_text = f'📞 Информация по номеру: {tel_number}\n'
    response_text = response_text + check_field('├ Страна: ', htmlweb_request.json()["country"]["name"], True)
    response_text = response_text + check_field('├ Город: ', htmlweb_request.json()["city"], True)
    response_text = response_text + check_field('├ Регион: ', htmlweb_request.json()["region"]["name"], False)
    response_text = response_text + check_field('├ Округ: ', htmlweb_request.json()["okrug"], False)
    response_text = response_text + check_field('├ Часовой пояс: ', htmlweb_request.json()["tz"], True)
    response_text = response_text + check_field('├ ОАО: ', htmlweb_request.json()["0"]["oper"], True)
    response_text = response_text + check_field('└ Оператор: ', htmlweb_request.json()["0"]["oper_brand"], True)

    print(response_text)

    bot.send_message(message.chat.id, 'response_text')

    bot.send_message(message.chat.id, response_text, parse_mode='Markdown')
    

bot.infinity_polling()