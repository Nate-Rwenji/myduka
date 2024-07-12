import psycopg2

# # connect to database
conn=psycopg2.connect(
    user = "postgres",
    dbname="myduka",
    password="2004-Grind",
    port=5432,
    host="localhost"
)
curr=conn.cursor()

def insert_products(values):
    insert="""insert into products(name,buying_price \
    ,selling_price,stock_quantity)values(%s,%s,%s,%s)"""
    curr.execute(insert,values)
    conn.commit()

def insert_sales(values):
    insert="insert into sales(pid,quantity,created_at) \
    values(%s,%s,now())"
    curr.execute(insert,values)
    conn.commit()
    
def profit_p():
    query="select products.name,sum((selling_price-buying_price)\
    * quantity) as profit from products join sales on products.id = sales.pid \
    group by products.name"
    curr.execute(query)
    data=curr.fetchall()
    return(data)


def profit_day():
    query="select date(sales.created_at) as sales_date,\
    sum((selling_price-buying_price)*quantity)as profits from products join sales on sales.pid=products.id group by sales_date order by sales_date asc"
    curr.execute(query)
    data=curr.fetchall()
    return(data)

def sales_product():
    query="select products.name,sales.quantity from products join sales on products.id=sales.id \
    order by products.name;"
    curr.execute(query)
    data=curr.fetchall()
    return(data)
    

def sales_day():
    query="select sales.quantity,sales.created_at from sales;"
    curr.execute(query)
    data=curr.fetchall()
    return(data)

def total_sales():
    query=" select sum(selling_price * quantity)as total_sales from products join sales on products.id=sales.pid;"
    curr.execute(query)
    data=curr.fetchall()
    print(data)
    return(data)

def get_data(table_name):
    curr.execute(f"select * from {table_name}")
    data=curr.fetchall()
    return data

def insert_info(values):
    query= "insert into users(full_name,email,password) VALUES(%s,%s,%s)"
    curr.execute(query,values)
    conn.commit()
    
def check_email(email):
    query= 'select * from users where email=%s'
    curr.execute(query,(email,))
    data=curr.fetchone()
    return data

def comp_email_and_password(email,password):
    query='select * from users where email=%s and password=%s'
    curr.execute(query,(email,password))
    data=curr.fetchall()
    return data