import mysql.connector,json

connection = mysql.connector.connect(
    host="localhost",
    port="3306",
    user="root",
    password="00000000", #輸入密碼
    database="TAIPEI"
)

cursor = connection.cursor() #cursor不要共用



with open("taipei-attractions.json", mode="r", encoding="utf-8") as file:
    data=json.load(file)
    result=data["result"]["results"]



for i in range(len(result)):
    dropHttps=result[i]["file"].split("https")
    # print(len(dropHttps))
    # print(dropHttps)
    list=[]
    for j in range(1,len(dropHttps)):
        addHttps="https"+dropHttps[j]
        if addHttps[-1]=="g" or addHttps[-1] =="G":
            list.append(addHttps)
    name=result[i]['name']
    category=result[i]['CAT']
    description=result[i]['description']
    address=result[i]['address']
    transport=result[i]['direction']
    mrt=result[i]['direction']
    lat=result[i]['latitude']
    lng=result[i]['longitude']
    sql="insert into webpage(name,category,description,address,transport,mrt,lat,lng,images) value(%s,%s,%s,%s,%s,%s,%s,%s,%s)"
    val=(name,category,description,address,transport,mrt,lat,lng,json.dumps(list))
    cursor.execute(sql,val)
    connection.commit()

