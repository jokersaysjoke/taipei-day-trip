from flask import *
from taipei_day_trip_module import taipei_database as db
from taipei_day_trip_module import taipei_jwt

bk=Blueprint("booking", __name__, static_folder="static", template_folder="/static")

@bk.route("/api/booking", methods=['GET']) #取得未確認下單的預定行程
def get_booking_info():
    try:
        connection_object = db.connection_pool.get_connection()
        cursor =  connection_object.cursor()      
        token=request.cookies.get("user")
        if token:
            response=taipei_jwt.jwt_decode()
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
            return {
                    "error": True,
                    "message": "未登入系統，拒絕存取"
                    }, 403
    except:
         return {
            "error": True,
            "message": "連線錯誤"}, 500
    finally:
        cursor.close()
        connection_object.close()

@bk.route("/api/booking", methods=['POST']) #建立新的預定行程
def new_booking():
    try:
        connection_object = db.connection_pool.get_connection()
        cursor =  connection_object.cursor()      
        token=request.cookies.get("user")
        if token:
            response=taipei_jwt.jwt_decode()
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

@bk.route("/api/booking", methods=['DELETE']) #刪除目前的預定行程
def del_booking():
    try:
        connection_object = db.connection_pool.get_connection()
        cursor =  connection_object.cursor()    
        token=request.cookies.get("user")
        if token:
            response=taipei_jwt.jwt_decode()
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
                    