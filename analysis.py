from database import *

# GET TOTAL 
def get_total_revenue():
    query = "select sum(amount) as total_amount from revenue"
    result = connect_sql(query)[0]['total_amount']
    return result

def get_total_expenses():
    query = "select sum(amount) as total_amount from expenses"
    result = connect_sql(query)[0]['total_amount']
    return result

def get_total_customers():
    query = "select count(*) as count from customers"
    result = connect_sql(query)[0]['count']
    return result

def get_total_profit():
    revenue = get_total_revenue()
    expense = get_total_expenses()
    profit = revenue - expense
    return profit

def get_user():
    query = "select * from users"
    result = connect_sql(query)[0]
    return result