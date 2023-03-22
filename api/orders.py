from flask import *
from taipei_day_trip_module import taipei_database as db
from taipei_day_trip_module import taipei_jwt
import datetime, requests

orders=Blueprint("orders", __name__, static_folder="static", template_folder="/static")

@orders.route("/api/orders", methods=['POST']) #建立新的訂單，並完成付款程序
def make_deal():
    try:
        connection_object = db.connection_pool.get_connection()
        cursor =  connection_object.cursor()      
        token=request.cookies.get("user")
        if token:
            response=taipei_jwt.jwt_decode()
            account_email=response['email']
            # 所有訂單資訊
            partner_key="partner_Mu7A1HlFQnZSjAUrHe2Kd88vrZZnEaI12XLHwqnGsRApRHPiSrFG3f4h"
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
            sql="INSERT INTO PAYMENT (ACCOUNT_EMAIL, ORDER_NUMBER, ORDER_PRICE, ATTRACTION_ID, ATTRACTION_NAME, ATTRACTION_ADDRESS, ATTRACTION_IMAGE, TRIP_DATE, TRIP_TIME, CONTACT_NAME, CONTACT_EMAIL, CONTACT_PHONE, STATUS) VALUE(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
            val=(
                account_email,
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

@orders.route("/api/orders/<int:orderNumber>", methods=['GET']) #根據訂單編號取得訂單資訊
def get_order_info(orderNumber):
    try:
        connection_object = db.connection_pool.get_connection()
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
                    return {"data":None}
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
