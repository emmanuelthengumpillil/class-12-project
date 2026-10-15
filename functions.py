import mysql.connector as Ms
import datetime
import credits as crd

def add_user():
    id = int(input("Enter Id: "))
    name = input("Enter Name: ")
    phone = input("Enter Phone: ")
    email = input("Enter Email: ")
    now = datetime.datetime.now()
    formatted_date = now.strftime(r"%Y-%m-%d")
    values = {"id":id, "name":name, "phone":phone, "email":email, "date":formatted_date}
    save_to_sql(values)


def delete_user():
    name = input("Enter Name: ")
    phone = input("Enter Phone: ")
    email = input("Enter Email: ")
    values = {"name":name, "phone":phone, "email":email, "table": 'customer'}
    remove_from_sql(values)

def sql(query):
    connector_obj = Ms.connect(host=crd.host, user=crd.user, password=crd.password, database=crd.database)
    cursor_obj = connector_obj.cursor()
    cursor_obj.execute(query)
    if query.strip().lower().startswith('select'):
        result = cursor_obj.fetchall()
        connector_obj.close()
        return result
    else:
        connector_obj.commit()
        connector_obj.close()
        return None
    
def show_from_sql(table):
    query = "Select * from {}".format(table)
    content = sql(query)
    print("--------------------")
    print("Table name:", table)

    for i in content:
        print(i)
    print("--------------------")

def save_to_sql(values):

    query1 = "Create table if not exists customer(id int primary key, name varchar(50) not null, phone char(12) not null, email varchar(100) not null, date_modified date not null)"
    query2 = "Insert into customer values({}, '{}', '{}', '{}', '{}')".format(values['id'], values['name'], values['phone'], values['email'], values['date'])
    sql(query1)
    sql(query2)
    print("Saved successfully")

def remove_from_sql(values):
    query = "delete from {} where name = '{}' and phone = '{}' and email = '{}'".format(values['table'], values['name'], values['phone'], values['email'])
    sql(query)
    show_from_sql(values['table'])
    print("Removed successfully")

