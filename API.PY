from flask import Flask, request,redirect,render_template
import mysql.connector

connection = mysql.connector.connect(
    host="localhost",
    port="3306",
    user="root",
    password="00000000", #輸入密碼
    database="TAIPEI",
    charset="utf8"
)

app=Flask(__name__)
app.secret_key="99TSLA"
app.config['JSON_AS_ASCII'] = False
# app.config['DEBUG'] = True

@app.route("/")  
def homePage():
    return render_template("index.html")


def pageKeyword(page,keyword):
    cursor=connection.cursor() #buffered=True , dictionary=True
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
        if attractionID:
            cursor=connection.cursor( )
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

@app.route("/api/categories") #取得景點分類名稱列表
def categories():
    try:
        cursor=connection.cursor()
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
app.run(port=3000)
