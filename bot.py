import telebot
import json
import os
import schedule
import threading
import time
from telebot import types

# 🔑 Токен от BotFather
TOKEN = "8106626064:AAHxXEKcqXij5BMhLdmO6A9t_vWAnTu3Mdc"
bot = telebot.TeleBot(TOKEN)

# 📁 Загрузка user_ids из файла, если он существует
if os.path.exists("users.json"):
    with open("users.json", "r") as f:
        user_ids = set(json.load(f))
else:
    user_ids = set()

# 💾 Сохраняем user_ids после изменений
def save_users():
    with open("users.json", "w") as f:
        json.dump(list(user_ids), f)

# 🟢 Обработка команды /start
@bot.message_handler(commands=['start'])
def handle_start(message):
    user_id = message.chat.id
    if user_id not in user_ids:
        user_ids.add(user_id)
        save_users()
    bot.send_message(user_id, "✅ Ты теперь подписан на рассылку материалов по английскому! 🎉")
    print(f"➕ Новый пользователь: {user_id}")

# 📬 Команда /send_material — вручную запускает рассылку
@bot.message_handler(commands=['send_material'])
def send_material(message):
    material = """
📚 *Английский на сегодня:*

🎯 Тема: Present Perfect
✅ Пример: _I have visited London._
📌 Используется, когда результат действия важен сейчас.

Увидимся завтра! 😉
"""
    for user_id in user_ids:
        try:
            bot.send_message(user_id, material, parse_mode='Markdown')
        except Exception as e:
            print(f"❗ Не удалось отправить {user_id}: {e}")

# 🔁 Авторассылка каждый день в 09:00
def send_daily_material():
    material = "🌞 Доброе утро! Вот материал на сегодня...\n\n📚 *Тема:* Future Simple\n✅ _I will learn English._"
    for user_id in user_ids:
        try:
            bot.send_message(user_id, material, parse_mode='Markdown')
        except Exception as e:
            print(f"Ошибка рассылки: {e}")

schedule.every().day.at("09:00").do(send_daily_material)

def scheduler():
    while True:
        schedule.run_pending()
        time.sleep(1)

# 🎛 Запускаем авторассылку в фоновом потоке
threading.Thread(target=scheduler).start()

# 🚀 Бот активен
bot.polling()
