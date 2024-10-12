import psycopg2
from secret import *
import telebot

def connection_open():
    conn = psycopg2.connect(
        database = "taskbot",
        host = 'localhost',
        user = "postgres",
        password = password1,
        port = 5432
    )
    return conn

def close_connection(conn,cur):
    cur.close()
    conn.close()





def create_db_users():
    conn = connection_open()
    cur = conn.cursor()
    cur.execute(
        """ create table if not exists users(
        user_id serial primary key,
        username varchar(100) unique,
        first_name varchar(100),
        last_name varchar(100),
        password varchar(100) unique);"""
    )
    conn.commit()
    close_connection(conn,cur)

def create_db_tasks():
    conn = connection_open()
    cur = conn.cursor()
    cur.execute(
        """
        create table if not exists tasks(
        task_id serial primary key,
        task_name varchar(100),
        duration varchar(100),
        is_done varchar(50) default False,
        chat_id varchar(20),
        username varchar(100) references users(username),
        password varchar(100) references users(password)
        );
        """
    )
    conn.commit()
    close_connection(conn,cur)

bot = telebot.TeleBot(API_KEY,parse_mode=None)

