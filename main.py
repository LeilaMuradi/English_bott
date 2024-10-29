import json
import random
import telebot

TOKEN = '7472754842:AAH393jQRRL0kCRejx0Y7W3ytf66cV6nE2k'

bot = telebot.TeleBot(TOKEN)

try:
    with open('user_data.json', 'r', encoding='utf-8') as file:
        user_data = json.load(file)
except FileNotFoundError:
    user_data = {}


@bot.message_handler(commands=['start'])
def handle_start(message):
    bot.send_message(message.chat.id, 'Приветик! Это твой телеграмм бот, скоро он будет уметь многое!')


@bot.message_handler(commands=['learn'])
def handle_learn(message):
    # bot.send_message(message.chat.id, user_data)
    user_words = user_data.get(str(message.chat.id), {})
    print(message)
    try:
        words_number = int(message.text.split()[1])
        ask_translation(message.chat.id, user_words, words_number)
    except ValueError:
        print("Ошибка: Введено не слово ")
    except IndexError:
        print("Ошибка: Введен не коректный индекс ")

def ask_translation(chat_id, user_words, words_left):
    if words_left > 0:
        word = random.choice(list(user_words.keys()))
        print(word)
        translation = user_words[word]
        bot.send_message(chat_id, f'Напищи перевод слова {word}')

        bot.register_next_step_handler_by_chat_id(chat_id, check_translation, translation, words_left)
    else:
        bot.send_message(chat_id, 'Это было полседние слово, поэтому урок завершен(')

    if len(user_words) == 0:
        bot.send_message(chat_id, 'В словаре ещё нету слов')


def check_translation(message, expected_translation, words_left):
    user_translation = message.text.strip().lower()
    if user_translation == expected_translation.lower():
        bot.send_message(message.chat.id, 'Правильно! Молодец!')
    else:
        bot.send_message(message.chat.id, f'Неправильно, правильный перевод {expected_translation}')
        ask_translation(message.chat.id, user_data[str(message.chat.id)], words_left-1)



@bot.message_handler(commands=['addword'])
def handle_addword(message):
    global user_data
    chat_id = message.chat.id
    user_dick = user_data.get(chat_id, {})


    words = message.text.split()[1:]
    if len(words) == 2:
        word, translation = words[0].lower(), words[1].lower()
        user_dick[word] = translation

        with open('user_data.json', 'r', encoding='utf-8') as file:
            data = json.load(file)
            print(data)

        user_data[str(chat_id)] = user_dick
        with open('user_data.json', 'w', encoding='utf-8') as file:
            json.dump(user_data, file, ensure_ascii=False, indent=4)
        bot.send_message(chat_id, f'Слово {word} довавленно в словарь')

    else:
        bot.send_message(chat_id, "Произошла ошибка. Попробуйте ещё раз")

# def handle_json():
#     with open('user_data.json', 'r', encoding='utf-8') as file:
#         data = json.load(file)
#         print(data[word])

@bot.message_handler(commands=['help'])
def handle_help(message):
    bot.send_message(message.chat.id, 'этот бот нужен для изучения английского язык'
                                      ' - в нем есть команды /learn, /start, /help')


@bot.message_handler(func=lambda message: True)
def handle_all(message):
    if message.text.lower() == 'как тебя зовут?':
        bot.send_message(message.chat.id, "У меня пока нету имени(")
    if message.text.lower() == 'Чем ты занимаешься?':
        bot.send_message(message.chat.id, "Я помогаю людям учить английский!")
    if message.text.lower() == 'Что ты любишь?':
        bot.send_message(message.chat.id, "Учиться, помогать людям и конечно познавать новое!")


if __name__ == '__main__':
    bot.polling(non_stop=True)
