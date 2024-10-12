from secret import *
from context import * 
from telebot import *
from telebot.types import ReplyKeyboardMarkup

create_db_users()
create_db_tasks()


@bot.message_handler(commands=['start','help'])
def welcome(message):
    btn1 = types.InlineKeyboardButton("add")
    btn2 = types.InlineKeyboardButton("get")
    btn3 = types.InlineKeyboardButton("get all")
    btn4 = types.InlineKeyboardButton("update")
    btn5 = types.InlineKeyboardButton("delete")
    btn6 = types.InlineKeyboardButton("reg")
    markup = ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    markup.row(btn6,btn1)
    markup.row(btn2,btn3)
    markup.row(btn4,btn5)
    bot.send_message(message.chat.id, "Welcome to tasks bot", reply_markup=markup)


@bot.message_handler(func=lambda message: True)
def handler(message):
    if message.text == "add":
        bot.send_message(message.chat.id, "Enter your task: ")
        bot.register_next_step_handler(message, ask_duration)
    elif message.text == "get":
        bot.send_message(message.chat.id, "enter task_id number to get: ")
        bot.register_next_step_handler(message,get_task)
    elif message.text == "get all":
        bot.send_message(message.chat.id, "Enter chat id to show all your task: ")
        bot.register_next_step_handler(message,get_all)
    elif message.text == "update":
        bot.send_message(message.chat.id,"Enter task_id to update: ")
        bot.register_next_step_handler(message,task_id)
    elif message.text == "delete":
        bot.send_message(message.chat.id, "Enter task id to delete it: ")
        bot.register_next_step_handler(message,delete)
    elif message.text == "reg":
        bot.send_message(message.chat.id, "Enter your password: ")
        global password
        password = message.text
        bot.register_next_step_handler(message,password_f)

# deleting
def delete(message):
    conn = connection_open()
    cur = conn.cursor()
    cur.execute(f""" delete from tasks where task_id = '{message.text}' """)
    conn.commit()
    close_connection(conn,cur)
    bot.send_message(message.chat.id, "deleted successfuly!")
# ----

# updating
def task_id(message):
    global old
    old = message.text
    bot.send_message(message.chat.id, "Enter new duration: ")
    bot.register_next_step_handler(message,update)

def update(message):
    conn = connection_open()
    cur = conn.cursor()
    cur.execute(f""" 
update tasks
set duration = '{message.text}' where task_id = '{old}' """)
    conn.commit()
    close_connection(conn,cur)
    bot.send_message(message.chat.id, "updated successfuly!")
# --


# all
def get_all(message):
    conn = connection_open()
    cur = conn.cursor()
    cur.execute(f"select * from tasks where chat_id = '{message.text}'")
    tasks = cur.fetchall()
    bot.send_message(message.chat.id, str(tasks))
    close_connection(conn,cur)
# --

# geeting 
def get_task(message):
    conn = connection_open()
    cur = conn.cursor()
    cur.execute(f"select * from tasks where task_id = '{message.text}'")
    task = cur.fetchone()
    bot.send_message(message.chat.id, str(task))
    close_connection(conn,cur)
# ---

# adding
def ask_duration(message):
    task_name = message.text
    bot.send_message(message.chat.id, "Enter task duration: ")
    bot.register_next_step_handler(message, lambda msg: is_done(msg, task_name))

def is_done(message, task_name):
    task_duration = message.text
    bot.send_message(message.chat.id, "Your task is done: True or False: ")
    bot.register_next_step_handler(message, lambda msg: add_task(msg, task_name, task_duration))

def add_task(message, task_name, task_duration):
    is_done = message.text
    chat_id = message.chat.id
    conn = connection_open()
    cur = conn.cursor()
    cur.execute("INSERT INTO tasks (task_name, duration, is_done, chat_id, username, password) VALUES (%s, %s, %s, %s, %s, %s)", (task_name, task_duration, is_done,chat_id,message.chat.username, password))
    conn.commit()
    close_connection(conn,cur)
    
    bot.send_message(message.chat.id, "Your task have been added successfully!")
# --


def password_f(message):
    bot.send_message(message.chat.id, "Your password was added!")
    conn = connection_open()
    cur = conn.cursor()
    cur.execute(f"""insert into users(username,first_name,last_name,password) values('{message.chat.username}','{message.chat.first_name}','{message.chat.last_name}','{password}')""")
    conn.commit()
    close_connection(conn,cur)

bot.infinity_polling()