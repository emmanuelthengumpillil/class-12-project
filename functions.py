import mysql.connector as Ms
import datetime

def add_user():
    name = input("Enter Name: ")
    phone = input("Enter Phone: ")
    email = input("Enter Email: ")
    time = datetime.datetime.now()
    values = {"name":name, "phone":phone, "email":email, "time":time}


def search_user():
    pass

def delete_user():
    pass

def sql(values):
    connector_obj = Ms.connect()