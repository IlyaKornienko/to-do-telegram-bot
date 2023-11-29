import telebot
import random
import sqlite3

# Токен телеграм бота який треба приховати
token = ''

bot = telebot.TeleBot(token)

RANDOM_TASKS = ["Зробити ToDo бота в Telegram", "Створити сайт на Wordpress", "Створити бот для відгуків клієнтів в Studio_Odintsovoy", "Створити сайт портфоліо", "Додати код в GitHub"]

HELP = """
/help - вивести список доступних команд;
/add - додати задачу;
/show - напечатать все добавленные задачи;
/random - добавить задачу на дату сегодня"""

tasks = {}

connection = sqlite3.connect("database", check_same_thread = True)
cursor = connection.cursor()

cursor.execute("CREATE TABLE IF NOT EXISTS Inventory_on (ID INT, 'Primary weapon' TEXT, 'Secondary weapon' TEXT)")
cursor.execute("CREATE TABLE IF NOT EXISTS Clans (Name TEXT, Points INT)")
cursor.execute("CREATE TABLE IF NOT EXISTS WorkStatus (ID INT, Status INT)")

connection.commit()
connection.close()

def add_todo(date, task):
  # Проверка даты в списке
  if date in tasks:
    tasks[date].append(task)
  # Если даты нет в списке добовляем дату в tasks
  else:
    tasks[date] = []
    tasks[date].append(task)

@bot.message_handler(commands=["help"])
def help(message):
    bot.send_message(message.chat.id, HELP)

@bot.message_handler(commands=["add"])
def add(message):
    command = message.text.split(maxsplit=2)
    date = command[1].lower()
    task = command[2]
    add_todo(date, task)
    text = "Задача " + task + " добавлена на дату " + date
    bot.send_message(message.chat.id, text)

@bot.message_handler(commands=["random"])
def random_add(message):
    date = "сегодня"
    task = random.choice(RANDOM_TASKS)
    add_todo(date, task)
    text = "Задача " + task + " добавлена на дату " + date
    bot.send_message(message.chat.id, text)

@bot.message_handler(commands=["show"])
def show(message):
    command = message.text.split(maxsplit=1)
    date = command[1].lower()
    text = ""
    if date in tasks:
        text = date.upper() + "\n"
        for task in tasks[date]:
            text = text + "[] " + task + "\n"
    else:
        text = "Задач на эту дату нет"
    bot.send_message(message.chat.id, text)

# Постоянно обращается к серверам
bot.polling(none_stop=True, interval=0)
