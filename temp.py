from flask import Flask,render_template,redirect,request,url_for,flash,session
from dbase import get_data,insert_products,insert_sales,profit_day,profit_p,insert_info,check_email,comp_email_and_password,sales_product,sales_day,total_sales
app=Flask(__name__)
app.secret_key='kenya'

@app.route("/")
@app.route("/index")
def index():
    return render_template("index.html")


@app.route("/next")
def next():
    return"hello rwenji"
# app.run(debug=True)

@app.route("/products")
def products():
    if "email" not in session:
        flash("Log in to access the page")
        return redirect(url_for("login")) 
    products=get_data('products')
    # print(products)
    return render_template("products.html",products=products)
# # app.run()
@app.route("/sales")
def sales():
    if "email" not in session:
        flash("Log in to access the page")
        return redirect(url_for("login")) 
    sales=get_data('sales')
    products=get_data('products')
    
    return render_template("sales.html",sales=sales,products=products)
# app.run(debug=True)
@app.route("/dashboard")
def dashboard():
    if "email" not in session:
        flash("Log in to access the pages")
        return redirect(url_for("login")) 
    
    pr_profit=profit_p()
    p_name=[]
    p_profit=[]
    for i in pr_profit:
        p_name.append(i[0])
        p_profit.append(float(i[1]))

        day_profit=profit_day()
        print(day_profit)
        dates=[]
        pr_day=[]
    for i in day_profit:
        dates.append(str(i[0]))
        pr_day.append(float(i[1]))

        p_s=sales_product()
        sales=[]
        prods=[]
    for i in p_s:
        sales.append(str(i[0]))
        prods.append(i[0])
        p_s=sales_product()
        

        s_d=sales_day()
        sale=[]
        day=[]
    for i in s_d:
        sale.append((i[0]))
        day.append((i[1]))
    s_d=sales_day()

    s_total=total_sales()
    for i in s_total:
        sl=round(i[0],2)

    return render_template("dashboard.html",p_name=p_name,pr_profit=p_profit,dates=dates,pr_day=pr_day,sales=sales,prods=prods,sale=sale,day=day,sl=sl)

@app.route("/add_prods",methods=["POST","GET"])
def add_products():
    p_name=request.form['pname']
    buying=request.form['buying']
    selling=request.form['selling']
    quantity=request.form['quantity']

    new_prods=(p_name,buying,selling,quantity)
    insert_products(new_prods)
    
    return redirect(url_for('products'))

@app.route("/make_sales",methods=["POST","GET"])
def add_sales():
    pid=request.form['pid']
    quantity=request.form['quantity']
    new_sales=(pid,quantity)
    insert_sales(new_sales)
    
    return redirect(url_for('sales'))
@app.route("/login",methods=["POST","GET"])
def login():
    if request.method=="POST":
        email=request.form['email']
        word=request.form['pass']
        e_mail=check_email(email)
        if e_mail==None:
            flash("email does not exist register")
            return redirect(url_for('register'))
        else:
             confirm=comp_email_and_password(email,word)
        if len(confirm)<1:
           flash("invalid email or password")
        else:
            session["email"]=email

            flash("login successfull")
            return redirect(url_for('dashboard'))
      
           
    return render_template("login.html")  
               
            
        
           
           
@app.route("/register",methods=["POST","GET"])
def register():
    if request.method=="POST":
        fname=request.form["fname" ]
        email=request.form["email"]
        word=request.form["word"]
        e_mail=check_email(email)
        if e_mail==None:
                user=(fname,email,word)
                insert_info(user)
                flash("registration successfull!!")
                return redirect(url_for("login"))
        else:
            flash("email already exists use a different email or login")
            if len(fname)<1:
                flash("Invalid Input")
                return redirect(url_for("register"))
            else:
                session["fname"]=fname

            flash("registration successfull")
            return redirect(url_for('login'))
    
    return render_template("register.html")
@app.route('/logout')
def logout():
    # remove the username from the session if it's there
    session.pop('email', None)
    flash("You are logged out")
    return redirect(url_for('login'))

   
        
        
       
app.run(debug=True)


