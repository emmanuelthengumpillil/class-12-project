import mysql.connector as Ms
import datetime
import credits

def add_user():
    id = int(input("Enter Id: "))
    name = input("Enter Name: ")
    phone = input("Enter Phone: ")
    email = input("Enter Email: ")
    now = datetime.datetime.now()
    formatted_date = now.strftime(r"%Y-%m-%d")
    values = {"id":id, "name":name, "phone":phone, "email":email, "date":formatted_date}
    save_to_sql(values)


def search_user():
    pass

def delete_user():
    pass

def save_to_sql(values):
    connector_obj = Ms.connect(host=credits.host, user=credits.user, password=credits.password, database=credits.database)
    cursor_obj = connector_obj.cursor()

    query1 = "Create table if not exists customer(id int primary key, name varchar(50) not null, phone char(12) not null, email varchar(100) not null, date_modified date not null)"
    query2 = "Insert into customer values({}, '{}', '{}', '{}', '{}')".format(values['id'], values['name'], values['phone'], values['email'], values['date'])

    cursor_obj.execute(query1)
    connector_obj.commit()
    cursor_obj.execute(query2)
    connector_obj.commit()

    connector_obj.close()
    print("Saved successfully")

add_user()