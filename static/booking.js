const body=document.querySelector("body")
const fakeBody=document.querySelector("#fakeBody")
const nav=document.querySelector(".nav")
const hi=document.querySelector(".hi")
const noInfo=document.querySelector(".noInfo")
const footer=document.querySelector("footer")
const attractionName=document.querySelector(".attractionName")
const attractionDate=document.querySelector(".attractionDate")
const attractionTime=document.querySelector(".attractionTime")
const attractionPrice=document.querySelectorAll(".attractionPrice")
const attractionAddress=document.querySelector(".attractionAddress")
const imgJPG=document.querySelector(".imgJPG")
const userName=document.querySelector(".userName")
const userEmail=document.querySelector(".userEmail")
const userPhone=document.querySelector(".userPhone")
const cardNumber=document.querySelector("#card-number")
const cardExpirationDate=document.querySelector("#card-expiration-date")
const cardCCV=document.querySelector("#card-ccv")
let attractionID="";
let ampm="";
// 刪除預設html
function delBookingInfo(){
    fakeBody.innerHTML="";
    noInfo.innerHTML="目前沒有任何待預定的行程";
    body.style.backgroundColor="#757575"
};
// 取得API資訊
function fetchBookingInfoAPI(){
    // let urls="http://127.0.0.1:3000";
    let urls="http://13.112.252.173:3000";

    fetch(urls+"/api/booking")
    .then(function(response){
        return response.json()
    })
    .then(function(data){
        let time="";
        console.log(data);
        if(data.data){
            if(data.data.time=="morning"){
                ampm="morning"
                time="早上 9 點到下午 4 點"
            }else{
                ampm="afternoon"
                time="下午 4 點到晚上 9 點"}
            attractionID=data.data.attraction.id
            imgJPG.setAttribute('src', data.data.attraction.image);
            attractionName.innerText=data.data.attraction.name;
            attractionDate.innerText=data.data.date;
            attractionTime.innerText=time;
            attractionPrice[0].innerText=data.data.price;
            attractionPrice[1].innerText=data.data.price;
            attractionAddress.innerText=data.data.attraction.address;

        }else{delBookingInfo()}
    })
};
fetchBookingInfoAPI();

// 刪除API資訊
function deleteAPI(){
    // let urls="http://127.0.0.1:3000";
    let urls="http://13.112.252.173:3000";

    fetch(urls+"/api/booking", {
        method:"DELETE"
    })
    .then(function(response){
        return response.json()
    })
    .then(function(data){
        console.log(data);
        if(data.ok){
            delBookingInfo();
        }
    })
};


function onSubmit() {
    // 讓 button click 之後觸發 getPrime 方法
    event.preventDefault()

    // 取得 TapPay Fields 的 status
    const tappayStatus = TPDirect.card.getTappayFieldsStatus()

    // 確認是否可以 getPrime
    if (tappayStatus.canGetPrime === false) {
        alert("請完整輸入資訊")
        return
    }

    // Get prime
    TPDirect.card.getPrime((result) => {
        if (result.status !== 0) {
            alert("請完整輸入資訊")
            return
        }
        if (userName.value=='' || userEmail.value=='' || userPhone.value==''){
            
            alert("請完整輸入使用者資訊")
        }else{
            prime=result.card.prime
            sendPrimeToServer(prime);
        }
        
        // send prime to your server, to pay with Pay by Prime API .
        // Pay By Prime Docs: https://docs.tappaysdk.com/tutorial/zh/back.html#pay-by-prime-api
    })
};

function sendPrimeToServer(prime){
    // let urls="http://127.0.0.1:3000";
    let urls="http://13.112.252.173:3000";

    fetch(urls+"/api/orders",{
        method:"POST",
        body:JSON.stringify({
            "prime": prime,
            "order":{
                "price":attractionPrice[1].innerText,
                "trip":{
                    "attraction":{
                        "id": attractionID,
                        "name": attractionName.innerText,
                        "address": attractionAddress.innerText,
                        "image": imgJPG.src
                    }

                },
                "date": attractionDate.innerText,
                "time": ampm
            },
            "contact":{
                "name": userName.value,
                "email": userEmail.value,
                "phone": userPhone.value
            }
        }),
        headers: new Headers({"Content-type":"application/json"})
    })
    .then(function(response){
        return response.json()
    })
    .then(function(data){
        console.log(data)
        if(data.data){
            number=data.data.number
            window.location.href=urls+'/thankyou'+"?number="+number;
        }
    })
};

