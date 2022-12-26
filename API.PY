from flask import *
import jwt
import time
import datetime
import mysql.connector
import requests


dbconfig = {
    "user" : "root",
    "password" : "00000000",
    "host" : "localhost",
    "database" : "TAIPEI",
}
# create connection pool
connection_pool = mysql.connector.pooling.MySQLConnectionPool(
    pool_name = "wehelp_pool",
    pool_size = 15,
    pool_reset_session = True,
    **dbconfig
)

app=Flask(__name__)
app.secret_key="99TSLA"
app.config['JSON_AS_ASCII'] = False
# app.config['DEBUG'] = True

@app.route("/")  
def homePage():
    return render_template("index.html")


def pageKeyword(page,keyword):
    try:
        connection_object = connection_pool.get_connection()
        cursor =  connection_object.cursor()        
        if keyword == None:
            cursor.execute("select * from webpage limit 12 offset %s",(page*12,))
            data=cursor.fetchall()
            cursor.execute("select * from webpage limit 12 offset %s",((page+1)*12,))
            nextPageData=cursor.fetchall()
            if len(nextPageData)!=0:
                nextPage=page+1
                list=[]
                for i in data[0:12]:
                    images=i[9].split(",")
                    dataDic={   
                                "id":i[0],
                                "name":i[1],
                                "category":i[2],
                                "description":i[3],
                                "address":i[4],
                                "transport":i[5],
                                "mrt":i[6],
                                "lat":i[7],
                                "lng":i[8],
                                "images":images
                            }
                    list.append(dataDic)
                return{"nextPage":nextPage,"data":list}

            elif len(nextPageData)==0:
                nextPage=None
                list=[]
                for i in data[0:12]:
                    images=i[9].split(",")
                    dataDic={   
                                "id":i[0],
                                "name":i[1],
                                "category":i[2],
                                "description":i[3],
                                "address":i[4],
                                "transport":i[5],
                                "mrt":i[6],
                                "lat":i[7],
                                "lng":i[8],
                                "images":images
                            }
                    list.append(dataDic)
                return{"nextPage":None,"data":list}
        elif keyword !=None:
            cursor.execute("select * from webpage where category=%s or name like %s limit 12 offset %s",(keyword,f'%{keyword}%',page*12))
            data=cursor.fetchall()
            cursor.execute("select * from webpage where category=%s or name like %s limit 12 offset %s",(keyword,f'%{keyword}%',(page+1)*12))
            nextPageData=cursor.fetchall()
            if len(nextPageData)!=0:
                nextPage=page+1
                list=[]
                for i in data[0:12]:
                    images=i[9].split(",")
                    dataDic={   
                                "id":i[0],
                                "name":i[1],
                                "category":i[2],
                                "description":i[3],
                                "address":i[4],
                                "transport":i[5],
                                "mrt":i[6],
                                "lat":i[7],
                                "lng":i[8],
                                "images":images
                            }
                    list.append(dataDic)
                return{"nextPage":nextPage,"data":list}
            elif len(nextPageData)==0:
                nextPage=None
                list=[]
                for i in data[0:12]:
                    images=i[9].split(",")
                    dataDic={   
                                "id":i[0],
                                "name":i[1],
                                "category":i[2],
                                "description":i[3],
                                "address":i[4],
                                "transport":i[5],
                                "mrt":i[6],
                                "lat":i[7],
                                "lng":i[8],
                                "images":images
                            }
                    list.append(dataDic)
                return{"nextPage":None,"data":list}
    except:
        print("Unexpected Error")
    finally:
        cursor.close()
        connection_object.close()
        
@app.route("/api/attractions") #取得景點資料列表
def getAttrations():
    try:
        if request.args.get("page"):
            page=int(request.args.get("page"))
            if request.args.get("keyword"):
                keyword=request.args.get("keyword")
                return pageKeyword(page,keyword)
            else:
                return pageKeyword(page=page,keyword=None)
    except:
            return{
                    "error": True,
                    "message": "伺服器錯誤"}, 500

@app.route("/api/attraction/<int:attractionID>") #根據景點編號取得景點資料
def getAttrationData(attractionID):
    try:
        connection_object = connection_pool.get_connection()
        cursor =  connection_object.cursor()        
        if attractionID:
            cursor.execute("select * from webpage where id= %s",(attractionID,))
            dataAttractionID=cursor.fetchall()
            if len(dataAttractionID)==0:
                return{
                        "error": True,
                        "message": "景點編號不正確"}, 400
            elif len(dataAttractionID)!=0:
                for i in dataAttractionID:
                    images=i[9].split(",")
                    return {"data":{
                                        "id":i[0],
                                        "name":i[1],
                                        "category":i[2],
                                        "description":i[3],
                                        "address":i[4],
                                        "transport":i[5],
                                        "mrt":i[6],
                                        "lat":i[7],
                                        "lng":i[8],
                                        "images":images
                                    }
                            }
        return{
                "error": True,
                "message": "景點編號不正確"}, 400
    
    except:
            return{
                    "error": True,
                    "message": "伺服器內部錯誤"}, 500
    finally:
        cursor.close()
        connection_object.close()

@app.route("/api/categories") #取得景點分類名稱列表
def categories():
    try:
        connection_object = connection_pool.get_connection()
        cursor =  connection_object.cursor()        
        cursor.execute("select distinct CATEGORY from webpage")
        data=cursor.fetchall()
        list=[]
        for i in data:
            for j in i:
                list.append(j)
        return {"data":list}
    except:
        return{
            "error": True,
            "message": "請按照情境提供對應的錯誤訊息"},500
    finally:
        cursor.close()
        connection_object.close()

@app.route("/attraction/<int:attractionID>") #根據景點編號移駕html
def turnToHtml(attractionID):
    if attractionID:
        return render_template("attraction.html")

@app.route("/api/user", methods=['POST']) #註冊一個新會員
def signUp():
    try:
        connection_object = connection_pool.get_connection()
        cursor =  connection_object.cursor()        
        if request.method=='POST':
            name=request.json["name"]
            email=request.json["email"]
            password=request.json["password"]
            cursor.execute("SELECT * FROM MEMBER WHERE EMAIL=%s",(email,))
            record=cursor.fetchone()
            if record:
                return {"error": True},400
            elif name==None or email==None or password==None:
                return {"error": True},400
            else:
                cursor.execute("INSERT INTO MEMBER(NAME, EMAIL, PASSWORD) VALUES (%s,%s,%s)",(name, email, password))
                connection_object.commit()
                return {"ok": True},200
        else:
             return {"error": True},400
    except:
           return {
            "error": True,
            "message": "連線錯誤"},500
    finally:
        cursor.close()
        connection_object.close()

@app.route("/api/user/auth", methods=['GET']) #取得當前登入會員資料
def getInfo():
    try:
        if request.method=='GET':
            token=request.cookies.get("user")
            response=jwt.decode(token, app.secret_key, algorithms=["HS256"])
            if response:
                id=response['id']
                name=response['name']
                email=response['email']
                return{"data":{'id':id,'name':name,'email':email}}
            else:
                return{"data":None}
    except:
            return{"data":None}

@app.route("/api/user/auth", methods=['PUT']) #登入
def signIn():
    try:
        connection_object = connection_pool.get_connection()
        cursor =  connection_object.cursor()        
        if request.method=='PUT':
            email=request.json["email"]
            password=request.json["password"]
            cursor.execute("SELECT * FROM MEMBER WHERE EMAIL=%s", (email,))
            record=cursor.fetchone()
            if record:
                if password==record[3]:
                    token=jwt.encode({
                        'id':record[0],
                        'name':record[1],
                        'email':record[2],
                        'expiretime':time.ctime()
                    }, app.secret_key, algorithm='HS256')
                    response=make_response({"ok":True},200)
                    response.set_cookie("user", token)
                    return response
                else:
                    return{"error":True},400
            else:
                return{"error":True},400
        else:
            return{"error":True},400
    except:
           return {
            "error": True,
            "message": "連線錯誤"},500
    finally:
        cursor.close()
        connection_object.close()

@app.route("/api/user/auth", methods=['DELETE']) #登出
def signOut():
    if request.method=="DELETE":
        response=make_response({"ok":True},200) #賦予response可以進出applicaiton
        response.delete_cookie('user')
        return response

@app.route("/api/booking", methods=['GET']) #取得未確認下單的預定行程
def get_booking_info():
    try:
        connection_object = connection_pool.get_connection()
        cursor =  connection_object.cursor()      
        token=request.cookies.get("user")
        if token:
            response=jwt.decode(token, app.secret_key, algorithms=["HS256"])
            email=response["email"]
            cursor.execute("select webpage.id, webpage.name, webpage.address, webpage.images, BOOKING.DATE, BOOKING.TIME, BOOKING.PRICE from webpage join BOOKING on webpage.id=BOOKING.ATTRACTIONID where BOOKING.EMAIL=%s" ,(email,))
            booking=cursor.fetchone()
            if booking:
                id=booking[0]
                name=booking[1]
                address=booking[2]
                image=booking[3].split(",")[0]
                date=booking[4]
                time=booking[5]
                price=booking[6]
                return {"data":{
                    "attraction":{
                        "id":id,
                        "name":name,
                        "address":address,
                        "image":image
                    },
                    "date":date,
                    "time":time,
                    "price":price
                }},200
            else:
                return {"data":None}
        else:
            return {"error":True}, 403
    except:
         return {
            "error": True,
            "message": "連線錯誤"}, 500
    finally:
        cursor.close()
        connection_object.close()

@app.route("/api/booking", methods=['POST']) #建立新的預定行程
def new_booking():
    try:
        connection_object = connection_pool.get_connection()
        cursor =  connection_object.cursor()      
        token=request.cookies.get("user")
        if token:
            response=jwt.decode(token, app.secret_key, algorithms=["HS256"])
            email=response["email"]
            attractionId=request.json["attractionId"]
            date=request.json["date"]
            time=request.json["time"]
            price=request.json["price"]
            cursor.execute("SELECT EMAIL FROM BOOKING WHERE EMAIL=%s", (email,))
            booking=cursor.fetchone()
            if booking:
                cursor.execute("UPDATE BOOKING SET ATTRACTIONID=%s, DATE=%s, TIME=%s, PRICE=%s WHERE EMAIL=%s", (attractionId, date, time, price, email,))
                connection_object.commit()
                return {"ok":True}
            if request.method=="POST":
                cursor.execute("INSERT INTO BOOKING(EMAIL, ATTRACTIONID, DATE, TIME, PRICE) VALUES (%s,%s,%s,%s,%s)", (email, attractionId, date, time, price))
                connection_object.commit()
                return {"ok":True}
            else:
                return {"error":True},400 #建立失敗，輸入不正確或其他原因
        else:
            return {"error":True},403 #未登入系統，拒絕存取
    except:
        return {
            "error": True,
            "message": "伺服器內部錯誤"}, 500
    finally:
        cursor.close()
        connection_object.close()

@app.route("/api/booking", methods=['DELETE']) #刪除目前的預定行程
def del_booking():
    try:
        connection_object = connection_pool.get_connection()
        cursor =  connection_object.cursor()    
        token=request.cookies.get("user")
        if token:
            response=jwt.decode(token, app.secret_key, algorithms=["HS256"])
            email=response["email"]
            cursor.execute("DELETE FROM BOOKING WHERE EMAIL=%s", (email,))
            connection_object.commit()
            return {"ok":True}, 200
        else:
            return {
                    "error": True,
                    "message": "未登入系統，拒絕存取"
                    }, 403
    except:
        return {
                "error": True,
                "message": "伺服器內部錯誤"}, 500
    finally:
        cursor.close()
        connection_object.close()
                    
@app.route("/booking", methods=['GET']) #取得未確認下單的預定行程
def booking_info():
    token=request.cookies.get("user")
    if token:
        response=jwt.decode(token, app.secret_key, algorithms=["HS256"])
        name=response['name']
        return render_template("booking.html", user=name)
    else:
        return redirect("/")

@app.route("/api/orders", methods=['POST']) #建立新的訂單，並完成付款程序
def make_deal():
    try:
        connection_object = connection_pool.get_connection()
        cursor =  connection_object.cursor()      
        token=request.cookies.get("user")
        if token:
            # 所有訂單資訊
            partner_key=""
            prime=request.json["prime"]
            order_number=datetime.datetime.now().strftime('%Y%m%d%H%M%S%f')
            order_price=request.json["order"]["price"]
            attraction_ID=request.json["order"]["trip"]["attraction"]["id"]
            attraction_name=request.json["order"]["trip"]["attraction"]["name"]
            attraction_address=request.json["order"]["trip"]["attraction"]["address"]
            attraction_image=request.json["order"]["trip"]["attraction"]["image"]
            trip_date=request.json["order"]["date"]
            trip_time=request.json["order"]["time"]
            contact_name=request.json["contact"]["name"]
            contact_email=request.json["contact"]["email"]
            contact_phone=request.json["contact"]["phone"]
            status=True #尚未付款或付款失敗為 1
            # 建立訂單資料庫
            sql="INSERT INTO PAYMENT (ORDER_NUMBER, ORDER_PRICE, ATTRACTION_ID, ATTRACTION_NAME, ATTRACTION_ADDRESS, ATTRACTION_IMAGE, TRIP_DATE, TRIP_TIME, CONTACT_NAME, CONTACT_EMAIL, CONTACT_PHONE, STATUS) VALUE(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
            val=(
                order_number, order_price, 
                attraction_ID, attraction_name, attraction_address, attraction_image,
                trip_date, trip_time, 
                contact_name, contact_email, contact_phone, 
                status,)
            cursor.execute(sql, val)
            connection_object.commit()
            # TapPay必填資訊
            info={
                    "prime": prime,
                    "partner_key": partner_key,
                    "merchant_id": "zz000ee_ESUN",
                    "order_number": order_number,
                    "amount": order_price,
                    "details": "台北一日遊",
                    "cardholder":{
                                "phone_number": contact_phone,
                                "name": contact_name,
                                "email": contact_email
                    },
                    "remember": False
                }
            # TapPay付款API，獲取TapPay回應
            url="https://sandbox.tappaysdk.com/tpc/payment/pay-by-prime"
            headers={
                'Content-Type': 'application/json',
                'x-api-key': partner_key
            }
            response=requests.post(url, headers=headers, json=info)
            res=response.json()
            # TapPay回應授權狀態
            if res["status"]==0:
                cursor.execute("UPDATE PAYMENT SET STATUS=%s", (False,))
                connection_object.commit()
                return {
                            "data": {
                                "number": order_number,
                                "payment": {
                                    "status": 0,
                                    "message": "付款成功"
                                }
                            }
                        }, 200
            else:
                return {
                        "error": True,
                        "number": order_number,
                        "status": res["status"],
                        "message": "訂單建立失敗，輸入不正確"}, 400
        else:
            return {
                    "error": True,
                    "message": "未登入系統，拒絕存取"}, 403
    except:
        return {
                "error": True,
                "message": "伺服器內部錯誤"}, 500
    finally:
        cursor.close()
        connection_object.close()

@app.route("/api/orders/<int:orderNumber>", methods=['GET']) #根據訂單編號取得訂單資訊
def get_order_info(orderNumber):
    try:
        connection_object = connection_pool.get_connection()
        cursor =  connection_object.cursor()      
        token=request.cookies.get("user")
        if token:
            if orderNumber:
                cursor.execute("SELECT * FROM PAYMENT WHERE ORDER_NUMBER=%s", (orderNumber,))
                order=cursor.fetchone()
                if order:
                    return{
                                "data": {
                                        "number": order[0],
                                        "price": order[1],
                                        "trip": {
                                                    "attraction": {
                                                                    "id": order[2],
                                                                    "name": order[3],
                                                                    "address": order[4],
                                                                    "image": order[5] 
                                                    },
                                                    "date": order[6],
                                                    "time": order[7]
                                        },
                                        "contact": {
                                                    "name": order[8],
                                                    "email": order[9],
                                                    "phone": order[10]
                                        },
                                        "status": order[11]
                                }
                            }, 200
                else:
                    {"data":None}
        else:
            return {
                    "error": True,
                    "message": "未登入系統，拒絕存取"}, 403
    except:
        return {
                "error": True,
                "message": "伺服器內部錯誤"}, 500
    finally:
        cursor.close()
        connection_object.close()

@app.route("/thankyou") #付款完成頁面
def thank_you_page():
    number=request.args.get("number")
    token=request.cookies.get("user")
    response=jwt.decode(token, app.secret_key, algorithms=["HS256"])
    if number:
        return render_template("thankyou.html", number=number)
    else:
        name=response['name']
        return render_template("booking.html", user=name)

app.run(port=3000)
