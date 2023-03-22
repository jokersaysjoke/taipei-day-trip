from flask import *
from taipei_day_trip_module import taipei_database as db
from taipei_day_trip_module import taipei_jwt
acc=Blueprint("account", __name__, static_folder="static", template_folder="/static")
app.secret_key="99TSLA"
@acc.route("/api/account")
def get_account_data():
    try:
        connection_object = db.connection_pool.get_connection()
        cursor =  connection_object.cursor()      
        token=request.cookies.get("user")
        if token:
            response=taipei_jwt.jwt_decode()
            email=response['email']
            cursor.execute("SELECT * FROM PAYMENT WHERE ACCOUNT_EMAIL=%s", (email,))
            orders=cursor.fetchall()
            if orders:
                result = {}
                list=[]
                for order in orders:
                    result["email"] = order[12]
                    result["number"] = order[0]
                    result["name"] = order[3]
                    result["date"] = order[6]
                    result["time"] = order[7]
                    result["price"] = order[1]
                    result["image"] = order[5]
                    list.append(result)
                return{
                    "data":list
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