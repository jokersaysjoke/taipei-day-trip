from flask import *
from taipei_day_trip_module import taipei_database as db
from taipei_day_trip_module import taipei_jwt
user=Blueprint("user", __name__, static_folder="static", template_folder="/static")
app.secret_key="99TSLA"

@user.route("/api/user", methods=['POST']) #註冊一個新會員
def signUp():
    try:
        connection_object = db.connection_pool.get_connection()
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

@user.route("/api/user/auth", methods=['GET']) #取得當前登入會員資料
def getInfo():
    try:
        if request.method=='GET':
            response=taipei_jwt.jwt_decode()
            if response:
                id=response['id']
                name=response['name']
                email=response['email']
                return{"data":{'id':id,'name':name,'email':email}}
            elif response==None:
                return{"data":None}
    except:
            return{"data":None}

@user.route("/api/user/auth", methods=['PUT']) #登入
def signIn():
    try:
        connection_object = db.connection_pool.get_connection()
        cursor =  connection_object.cursor()        
        if request.method=='PUT':
            email=request.json["email"]
            password=request.json["password"]
            cursor.execute("SELECT * FROM MEMBER WHERE EMAIL=%s", (email,))
            record=cursor.fetchone()
            if record and password==record[3]:
                response=taipei_jwt.jwt_encode(record[0],record[1],record[2])
                return response
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

@user.route("/api/user/auth", methods=['DELETE']) #登出
def signOut():
    if request.method=="DELETE":
        response=make_response({"ok":True},200) #賦予response可以進出applicaiton
        response.delete_cookie('user')
        return response
