import sqlite3
import time
import math

class FDataBase:
    def __init__(self, db):
        self.__db = db
        self.__cur = db.cursor()


    def addMessage(self, name, text):
        try:
            tm = math.floor(time.time())
            self.__cur.execute("INSERT INTO messages VALUES(NULL, ?, ?, ?)", (name, text, tm))
            self.__db.commit()
        except sqlite3.Error as e:
            print("Ошибка добавления статьи в БД "+str(e))
            return False
        return True

    def getHistoryMessages(self):
        try:
            self.__cur.execute(f"SELECT name, text, datetime(time, 'unixepoch') as tm FROM messages ORDER BY tm DESC")
            res = self.__cur.fetchall()
            if res: return res
        except sqlite3.Error as e:
            print("Ошибка получения статьи из БД "+str(e))
        return []
