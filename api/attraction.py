from flask import *
from taipei_day_trip_module import taipei_database as db

att=Blueprint("attraction", __name__, static_folder="static", template_folder="/static")

def pageKeyword(page,keyword):
    try:
        connection_object = db.connection_pool.get_connection()
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
        
@att.route("/api/attractions") #取得景點資料列表
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

@att.route("/api/attraction/<int:attractionID>") #根據景點編號取得景點資料
def getAttrationData(attractionID):
    try:
        connection_object = db.connection_pool.get_connection()
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

@att.route("/api/categories") #取得景點分類名稱列表
def categories():
    try:
        connection_object = db.connection_pool.get_connection()
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