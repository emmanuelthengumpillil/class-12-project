import mysql.connector as Ms
import datetime
import credits as crd

def add_user(user):
    now = datetime.datetime.now()
    formatted_date = now.strftime(r"%Y-%m-%d")
    values = {"id":user.id, "name":user.name, "phone":user.phone, "email":user.email, "date":formatted_date}

    query1 = "Create table if not exists customer(id int primary key, name varchar(50) not null, phone char(12) not null, email varchar(100) not null, date_modified date not null)"
    query2 = "Insert into customer values({}, '{}', '{}', '{}', '{}')".format(values['id'], values['name'], values['phone'], values['email'], values['date'])
    connect_sql(query1)
    connect_sql(query2)
    print("Saved successfully")
    return values

def delete_user(user):
    values = {"name":user.name, "phone":user.phone, "email":user.email, "table": 'customer'}
    query = "delete from {} where name = '{}' and phone = '{}' and email = '{}'".format(values['table'], values['name'], values['phone'], values['email'])
    connect_sql(query)
    show_from_sql(values['table'])
    print("Removed successfully")
    return values

def search_user():
    pass

def connect_sql(query):
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
    content = connect_sql(query)
    return content

