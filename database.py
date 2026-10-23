import mysql.connector as Ms
import datetime
import credits as crd

# ADD CUSTOMER
def add_customer(user):
    now = datetime.datetime.now()
    formatted_date = now.strftime(r"%Y-%m-%d")
    values = {"name":user['name'], "phone":user['phone'], "email":user['email'], "date":formatted_date}
    table_name = 'customers'

    query1 = "Insert into {} (name, phone, email, date_modified) values('{}', '{}', '{}', '{}')".format(table_name, values['name'], values['phone'], values['email'], values['date'])
    connect_sql(query1)
    print("Saved successfully")
    return values

# DELETE CUSTOMER
def delete_customer(id):
    table_name = 'customers'
    query = "delete from {} where id = '{}'".format(table_name, id)
    connect_sql(query)
    show_from_sql()
    return "Removed Successfully"

# EDIT USER
def edit_customer(values):
    table_name = "customers"
    query = "Update {} set name = '{}', phone = {}, email = '{}' where id = {}".format(table_name, values['name'], values['phone'], values['email'], values['id'])
    connect_sql(query)
    return values

# SEARCH USER
def search_customers_by_name(values):
    table_name = 'customers'
    query = "Select * from {} where name like '{}%'".format(table_name, values['name'])
    result = connect_sql(query)
    print(result)
    return result

def search_customers_by_id(values):
    table_name = 'customers'
    query = "Select * from {} where id = {}".format(table_name, values['id'])
    result = connect_sql(query)
    return result

def connect_sql(query):
    connector_obj = Ms.connect(host=crd.host, user=crd.user, password=crd.password, database=crd.database)
    if connector_obj.is_connected():
        cursor_obj = connector_obj.cursor(dictionary=True)
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
    database_name = crd.database
    table_name = 'customer'

    query1 = "Create database if not exists {}".format(database_name)
    connect_sql(query1)
    query2 = "Use {}".format(database_name)
    connect_sql(query2)
    query3 = "Create table if not exists {}(id int auto_increment primary key, name varchar(75) not null, phone char(12) not null, email varchar(255) not null, date_modified date not null)".format(table_name)
    connect_sql(query3)
    message = "MySql setup successfull"
    return message

def show_from_sql():
    table_name = 'customers'
    query = "Select * from {} order by id".format(table_name)
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
