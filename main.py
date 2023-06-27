from flask import Flask, render_template, request, redirect, url_for, session
import sqlite3
from datetime import date
from flask_session import Session

con = sqlite3.connect("canteen.db", check_same_thread=False)
con.row_factory = sqlite3.Row
cur = con.cursor()

app = Flask(__name__)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

today = date.today()


@app.route('/', methods=['POST', 'GET'])
def index():
    if request.method == 'POST':
        usernm = request.form['unm']
        passwd = request.form['pwd']
        if usernm == "admin" and passwd == "admin":
            return redirect('/admin_home')
        else:
            cur.execute("select * from login")
            res = cur.fetchall()
            for i in res:
                if i[1] == usernm and i[2] == passwd and i[3] == "staff":
                    return redirect(url_for('staff_home', u=usernm))
                elif i[1] == usernm and i[2] == passwd and i[3] == "user":
                    print(i[1], i[3], i[2])
                    return redirect(url_for('user_home', u=usernm))
            else:
                return redirect("/")
    return render_template("index.html")


@app.route('/admin_home')
def admin_home():
    return render_template("admin_home.html")


@app.route('/user_home/<u>')
def user_home(u):
    global res
    cur.execute("select * from user where admno='" + u + "'")
    res = cur.fetchall()
    session["uid"] = res[0][0]
    session["uname"] = res[0][2]
    return render_template("user_home.html", data=res[0])


@app.route('/user_home1')
def user_home1():
    return render_template("user_home.html", data=res[0])


@app.route('/staff_home/<u>')
def staff_home(u):
    global res
    cur.execute("select * from staff where usernm='" + u + "'")
    res = cur.fetchall()
    return render_template("staff_home.html", data=res[0])


@app.route('/staff_home1')
def staff_home1():
    return render_template("staff_home.html", data=res[0])


@app.route('/new_staff', methods=['POST', 'GET'])
def new_staff():
    cur.execute("select * from staff")
    output = cur.fetchall()
    return render_template("new_staff.html", res=output)


@app.route('/add_staff', methods=['POST', 'GET'])
def add_staff():
    if request.method == 'POST':
        snm = request.form['snm']
        smob = request.form['smob']
        semail = request.form['semail']
        sunm = request.form['sunm']
        spwd = request.form['spwd']
        con.execute(
            "create table if not exists staff(SID integer primary key autoincrement,name varchar(50),mob varchar(20),email varchrar(50),usernm varchar(50),passwd varchar(50))"
        )
        con.execute(
            "create table if not exists login (id integer primary key autoincrement,usernm varchar(20),passwd varchar(20),role varchar(20))"
        )
        cur.execute(
            "insert into staff(name,mob,email,usernm,passwd) values('" + snm +
            "','" + smob + "','" + semail + "','" + sunm + "','" + spwd + "')")
        con.commit()
        cur.execute("insert into login(usernm,passwd,role) values('" + sunm +
                    "','" + spwd + "','staff')")
        con.commit()
        return redirect('/new_staff')
    return render_template("add_staff.html")


@app.route('/edit_staff/<int:id>', methods=['POST', 'GET'])
def edit_staff(id):
    cur.execute("select * from staff where SID='" + str(id) + "'")
    res = cur.fetchall()
    return render_template("edit_staff.html", data=res)


@app.route('/edit_staff1', methods=['POST', 'GET'])
def edit_staff1():
    if request.method == 'POST':
        id = request.form['sid1']
        snm = request.form['snm']
        smob = request.form['smob']
        semail = request.form['semail']
        sunm = request.form['sunm']
        spwd = request.form['spwd']
        cur.execute("update staff set name='" + snm + "',mob='" + smob +
                    "',email='" + semail + "',usernm='" + sunm + "',passwd='" +
                    spwd + "' where SID='" + str(id) + "'")
        con.commit()
        return redirect('/new_staff')
    return render_template("edit_staff.html")


@app.route('/delete_staff/<int:id>', methods=['POST', 'GET'])
def delete_staff(id):
    cur.execute("delete from staff where SID='" + str(id) + "'")
    con.commit()
    return redirect('/new_staff')


@app.route('/view_user')
def view_user():
    cur.execute(
        "SELECT count(*) FROM sqlite_master WHERE type='table' AND name='user';"
    )
    r = cur.fetchall()
    if r[0][0] == 0:
        return render_template("view_user.html")
    else:
        cur.execute("select * from user")
        output = cur.fetchall()
        return render_template("view_user.html", res=output)


@app.route('/add_user', methods=['POST', 'GET'])
def add_user():
    if request.method == 'POST':
        admno = request.form['admno']
        unm = request.form['unm']
        dept = request.form['dept']
        batch = request.form['batch']
        umob = request.form['umob']
        uemail = request.form['uemail']
        upwd = request.form['upwd']
        con.execute(
            "create table if not exists user(UID integer primary key autoincrement,admno integer unique,name varchar(50),dept varchar(50),batch varchar(20),mob varchar(20),email varchrar(50),passwd varchar(50))"
        )
        cur.execute(
            "insert into user(admno,name,dept,batch,mob,email,passwd) values('"
            + admno + "','" + unm + "','" + dept + "','" + batch + "','" +
            umob + "','" + uemail + "','" + upwd + "')")
        con.commit()
        cur.execute("insert into login(usernm,passwd,role) values('" + admno +
                    "','" + upwd + "','user')")
        con.commit()
        return redirect('/view_user')
    return render_template("add_user.html")


@app.route('/edit_user/<int:id>', methods=['POST', 'GET'])
def edit_user(id):
    cur.execute("select * from user where UID='" + str(id) + "'")
    res = cur.fetchall()
    return render_template("edit_user.html", data=res)


@app.route('/edit_user1', methods=['POST', 'GET'])
def edit_user1():
    if request.method == 'POST':
        uid = request.form['uid1']
        admno = request.form['admno']
        unm = request.form['unm']
        dept = request.form['dept']
        batch = request.form['batch']
        umob = request.form['umob']
        uemail = request.form['uemail']
        upwd = request.form['upwd']
        cur.execute("update user set admno='" + admno + "',name='" + unm +
                    "',dept='" + dept + "',batch='" + batch + "',mob='" +
                    umob + "',email='" + uemail + "',passwd='" + upwd +
                    "' where UID='" + uid + "'")
        con.commit()
        return redirect('/view_user')
    return render_template("edit_user.html")


@app.route('/delete_user/<int:id>', methods=['POST', 'GET'])
def delete_user(id):
    cur.execute("delete from user where UID='" + str(id) + "'")
    con.commit()
    return redirect('/view_user')


# Item


@app.route('/new_item', methods=['POST', 'GET'])
def new_item():
    return render_template("new_item.html")


@app.route('/add_item', methods=['POST', 'GET'])
def add_item():
    if request.method == 'POST':
        ic = request.form['icode']
        it = request.form['iname']
        ip = request.form['iprice']
        con.execute(
            "create table if not exists item(item_code integer primary key,item_name varchar(50),item_price integer)"
        )
        cur.execute("insert into item values(" + ic + ",'" + it + "'," + ip +
                    ")")
        con.commit()
        return redirect('/new_item')
    return render_template("add_item.html")


@app.route('/view_item', methods=['POST', 'GET'])
def view_item():
    cur.execute("select * from item")
    data = cur.fetchall()
    return render_template("staff_item.html", res=data)


@app.route('/item_stock', methods=['POST', 'GET'])
def item_stock():
    if request.method == 'POST':
        ic = request.form['iid1']
        stk1 = request.form['stk']
        cur.execute("select * from item where item_code='" + ic + "'")
        item1 = cur.fetchall()
        con.execute(
            "create table if not exists stock_item(stock_id integer primary key autoincrement,item_code integer,item_name varchar(50),item_price integer,item_qty integer,avail_qty integer,date_stock date)"
        )
        today = date.today()
        cur.execute(
            "insert into stock_item (item_code,item_name,item_price,item_qty,avail_qty,date_stock) values("
            + str(ic) + ",'" + item1[0][1] + "'," + str(item1[0][2]) + "," +
            str(stk1) + "," + str(stk1) + ",'" + str(today) + "')")
        con.commit()
        return redirect('/view_item')
    return render_template("staff_item.html")


@app.route('/edit_item/<int:id>', methods=['POST', 'GET'])
def edit_item(id):
    cur.execute("select * from item where item_code='" + str(id) + "'")
    res = cur.fetchall()
    return render_template("edit_item.html", data=res)


@app.route('/edit_item1', methods=['POST', 'GET'])
def edit_item1():
    if request.method == 'POST':
        ic = request.form['icode']
        it = request.form['iname']
        ip = request.form['iprice']
        cur.execute("update item set item_name='" + it + "',item_price=" + ip +
                    " where item_code=" + ic + "")
        con.commit()
        return redirect('/view_item')
    return render_template("edit_item.html")


@app.route('/delete_item/<int:id>', methods=['POST', 'GET'])
def delete_item(id):
    cur.execute("delete from item where item_code='" + str(id) + "'")
    con.commit()
    return redirect('/view_item')


@app.route('/user_order', methods=['POST', 'GET'])
def user_order():
    today = date.today()
    cur.execute("select * from stock_item where date_stock='" + str(today) +
                "'")
    data = cur.fetchall()
    return render_template("user_order.html", res=data)


order = []


@app.route('/user_order1', methods=['POST', 'GET'])
def user_order1():
    if request.method == 'POST':
        sid = request.form['sid1']
        qty1 = request.form['qty']
        inm = request.form['iname']
        order.append([sid, qty1, inm])
        return redirect("/user_order")
    return render_template("user_order.html")


@app.route('/confirm_order', methods=['POST', 'GET'])
def confirm_order():
    return render_template("order_confirm.html", res=order)


@app.route('/remove_order/<id>')
def remove_order(id):
    for i in order:
        if i[0] == id:
            order.remove(i)
    return redirect('/confirm_order')


@app.route('/submit_order', methods=['POST', 'GET'])
def submit_order():
    con.execute(
        "create table if not exists order_item(id integer primary key autoincrement,user_id integer,user_name varchar(50),item_code integer,item_name varchar(50),item_price integer,item_qty integer,order_date date,token_no integer,status integer,payment_mode varchar(40))"
    )
    today = date.today()
    cur.execute("select max(token_no) from order_item where order_date='" +
                str(today) + "'")
    res = cur.fetchall()
    if res[0][0] == None:
        tno = 1
    else:
        tno = int(res[0][0]) + 1
    uid1 = session["uid"]
    uname1 = session["uname"]
    t = 0
    for i in order:
        cur.execute("select * from stock_item where stock_id=" + i[0] + "")
        data = cur.fetchall()
        con.execute(
            "insert into order_item(user_id,user_name,item_code,item_name,item_price,item_qty,order_date,token_no,status) values("
            + str(uid1) + ",'" + uname1 + "'," + str(data[0][1]) + ",'" +
            data[0][2] + "'," + str(data[0][3]) + "," + str(i[1]) + ",'" +
            str(today) + "'," + str(tno) + ",0)")
        con.commit()
        cur.execute("update stock_item set avail_qty=avail_qty-" + str(i[1]) +
                    " where stock_id=" + str(i[0]) + "")
        con.commit()
        t = t + (int(data[0][3]) * int(i[1]))
    order.clear()
    return render_template("user_token.html", res2=[t, tno])


@app.route('/payment', methods=['POST', 'GET'])
def payment():
    if request.method == 'POST':
        mop = request.form['mop']
        tno = request.form['tno']
        print(mop, tno)
        cur.execute("update order_item set payment_mode='" + mop +
                    "' where token_no=" + str(tno) + " and order_date='" +
                    str(today) + "'")
        con.commit()
        return redirect('/user_history')
    return render_template("user_token.html")


@app.route('/view_order', methods=['POST', 'GET'])
def view_order():
    cur.execute(
        "select distinct(token_no) from order_item where order_date='" +
        str(today) + "' and status=0")
    res = cur.fetchall()
    return render_template("view_order.html", tno=res)


@app.route('/display_order/<tno>')
def display_order(tno):
    cur.execute("select * from order_item where order_date='" + str(today) +
                "' and token_no=" + str(tno) + "")
    res = cur.fetchall()
    t = 0
    for i in res:
        t = t + (int(i[5]) * int(i[6]))
    return render_template("display_order.html", data=[res, t])


@app.route('/accept_order/<tno>')
def accept_order(tno):
    cur.execute("update order_item set status=1 where order_date='" +
                str(today) + "' and token_no=" + str(tno) + "")
    con.commit()
    return redirect("/view_order")


@app.route('/reject_order/<tno>')
def reject_order(tno):
    cur.execute("update order_item set status=-1 where order_date='" +
                str(today) + "' and token_no=" + str(tno) + "")
    con.commit()
    cur.execute("select * from order_item where order_date='" + str(today) +
                "' and token_no=" + str(tno) + "")
    res = cur.fetchall()
    for i in res:
        cur.execute("update stock_item set avail_qty=avail_qty+" + str(i[6]) +
                    " where  date_stock='" + str(today) + "' and item_code=" +
                    str(i[3]) + "")
        con.commit()
    return redirect("/view_order")


@app.route('/order_history')
def order_history():
    cur.execute("select * from order_item order by id desc")
    data = cur.fetchall()
    return render_template("order_history.html", res=data)


@app.route('/user_history')
def user_history():
    uid1 = session["uid"]
    cur.execute("select * from order_item where user_id=" + str(uid1) +
                " order by id desc")
    data = cur.fetchall()
    return render_template("user_history.html", res=data)


app.run(host='0.0.0.0', port=81)
