from flask import *
import jwt, sys
sys.path.append("taipei_day_trip_module")
sys.path.append("api")
from api.attraction import att
from api.user import user
from api.booking import bk
from api.orders import orders
from api.account import acc

app=Flask(__name__)
app.secret_key="99TSLA"
app.config['JSON_AS_ASCII'] = False
# app.config['DEBUG'] = True
app.register_blueprint(att)
app.register_blueprint(user)
app.register_blueprint(bk)
app.register_blueprint(orders)
app.register_blueprint(acc)


@app.route("/")  
def homePage():
    return render_template("index.html")

@app.route("/attraction/<int:attractionID>") #根據景點編號移駕html
def turnToHtml(attractionID):
    if attractionID:
        return render_template("attraction.html")

@app.route("/booking") #取得未確認下單的預定行程
def booking_info():
    token=request.cookies.get("user")
    if token:
        response=jwt.decode(token, app.secret_key, algorithms=["HS256"])
        name=response['name']
        return render_template("booking.html", user=name)
    else:
        return redirect("/")

@app.route("/thankyou") #付款完成頁面
def thank_you_page():
    number=request.args.get("number")
    token=request.cookies.get("user")
    if token:
        if number:
            return render_template("thankyou.html", number=number)
        else:
            return redirect("/booking")
    else:
        return redirect("/")

@app.route("/account") #會員中心
def user_page():
    token=request.cookies.get("user")
    if token:
        response=jwt.decode(token, app.secret_key, algorithms=["HS256"])
        name=response['name']
        return render_template("account.html")
    else:
        return redirect("/")

app.run(port=3000)
