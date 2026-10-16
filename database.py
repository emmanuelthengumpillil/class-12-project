import mysql.connector as Ms
import datetime
import credits as crd

def add_user(user):
    now = datetime.datetime.now()
    formatted_date = now.strftime(r"%Y-%m-%d")
    values = {"name":user.name, "phone":user.phone, "email":user.email, "date":formatted_date}

    query1 = "Insert into customer values({}, '{}', '{}', '{}', '{}')".format(values['id'], values['name'], values['phone'], values['email'], values['date'])
    connect_sql(query1)
    print("Saved successfully")
    return values

def delete_user(user):
    values = {"name":user.name, "phone":user.phone, "email":user.email, "table": 'customer'}
    query = "delete from {} where name = '{}' and phone = '{}' and email = '{}'".format(values['table'], values['name'], values['phone'], values['email'])
    connect_sql(query)
    show_from_sql(values['table'])
    print("Removed successfully")
    return values

def search_user(user):
    query = "Select * from customer where name like '{}%'".format(user.name)
    result = connect_sql(query)
    print(result)
    return result

def connect_sql(query):
    connector_obj = Ms.connect(host=crd.host, user=crd.user, password=crd.password)
    if connector_obj.is_connected():
        cursor_obj = connector_obj.cursor()
        cursor_obj.execute(query)
        if query.strip().lower().split()[0] in ['select', 'show', 'desc', 'describe']:
            result = cursor_obj.fetchall()
            connector_obj.close()
            return result
        else:
            connector_obj.commit()
            connector_obj.close()
            return None
    else:
        message = "Connection Failed"
        return message

def setup_sql():
    database = crd.database()
    query1 = "Create database if not exists {}".format(database)
    connect_sql(query1)
    query2 = "Use {}".format(database)
    connect_sql(query2)
    query3 = "Create table if not exists customer(id int auto_increment primary key, name varchar(75) not null, phone char(12) not null, email varchar(255) not null, date_modified date not null)"
    connect_sql(query3)
    message = "MySql setup successfull"
    return message

def show_from_sql(table):
    query = "Select * from {}".format(table)
    content = connect_sql(query)
    return content

def show_tables():
    query = "show tables"
    result = connect_sql(query)
    return result

def desc_table(tablename):
    query = "desc {}".format(tablename)
    result = connect_sql(query)
    return result
