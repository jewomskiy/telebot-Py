import pymysql
from pymysql import OperationalError, InterfaceError
from pymysql.cursors import DictCursor
import json


class MyLink:

    def __init__(self, host, login, password, db):
        self.host = host
        self.login = login
        self.password = password
        self.db = db
        self.link = None
        self.link = self.Auth()

    def Auth(self):
        if self.link is not None:
            self.link.close()

        return pymysql.connect(
            host=self.host,
            user=self.login,
            password=self.password,
            db=self.db,
            charset='cp1251',
            cursorclass=DictCursor
        )

    def Insert(self, table: str, array: dict):

        cursor = self.link.cursor()
        query = "INSERT INTO " + table

        keys = ""
        values = ""

        for key in array.keys():
            if keys != "":
                keys += ","
                values += ","

            keys += str(key)
            values += "'" + str(array[key]) + "'"

        query = query + " (" + keys + ") VALUES(" + values + ")"
        flag = True
        while flag:
            try:
                cursor.execute(query)
                flag = False
            except OperationalError as e:
                print('Не удалось выполнить: ' + query)
                self.link = self.Auth()
                cursor = self.link.cursor()
            except InterfaceError as e:
                self.link = self.Auth()
                cursor = self.link.cursor()

        self.link.commit()

    def Select(self, table: str, where: str = ""):

        cursor = self.link.cursor()
        query = "SELECT * FROM " + table

        if where != "":
            query += " WHERE " + where

        flag = True
        while flag:
            try:
                cursor.execute(query)
                flag = False
            except OperationalError as e:
                print('Не удалось выполнить: ' + query)
                self.link = self.Auth()
                cursor = self.link.cursor()
            except InterfaceError as e:
                self.link = self.Auth()
                cursor = self.link.cursor()

        result = []

        for row in cursor:
            result.append(row)

        return result

    def Update(self, table: str, array: dict, where: str):

        cursor = self.link.cursor()
        query = "UPDATE " + table + " SET "

        set = ""

        for key in array.keys():
            if set != "":
                set += ","

            set += str(key) + "='" + str(array[key]) + "'"

        query += set
        query += " WHERE " + where

        flag = True
        while flag:
            try:
                cursor.execute(query)
                flag = False
            except OperationalError as e:
                print('Не удалось выполнить: ' + query)
                self.link = self.Auth()
                cursor = self.link.cursor()
            except InterfaceError as e:
                self.link = self.Auth()
                cursor = self.link.cursor()

        self.link.commit()

    def Delete(self, table, where):

        cursor = self.link.cursor()
        query = "DELETE FROM " + table + " WHERE " + where

        flag = True
        while flag:
            try:
                cursor.execute(query)
                flag = False
            except OperationalError as e:
                print('Не удалось выполнить: ' + query)
                self.link = self.Auth()
                cursor = self.link.cursor()
            except InterfaceError as e:
                self.link = self.Auth()
                cursor = self.link.cursor()

        self.link.commit()