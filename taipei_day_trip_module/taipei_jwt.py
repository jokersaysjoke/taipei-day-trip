from flask import make_response, request
import jwt, time

def jwt_decode():
    token=request.cookies.get("user")
    response=jwt.decode(token, "99TSLA", algorithms=["HS256"])
    if response:
        return response
    return {"response":None}

def jwt_encode(id, name, email):
    token=jwt.encode({
                    'id':id,
                    'name':name,
                    'email':email,
                    'expiretime':time.ctime()
                }, "99TSLA", algorithm='HS256')
    response=make_response({"ok":True},200)
    response.set_cookie("user", token)
    return response
