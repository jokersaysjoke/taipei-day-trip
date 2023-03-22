const body=document.querySelector("body")
const fakeBody=document.querySelector("#fakeBody")
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
let attractionID="";
let ampm="";
// 刪除預設html
function delBookingInfo(){
    const noInfo=document.querySelector(".noInfo")
    fakeBody.innerHTML=""
    noInfo.textContent="目前沒有任何待預定的行程";
    body.style.backgroundColor="#757575";
};
// fetch booking API
async function fetchBookingInfoAPI(){
    const response=await fetch(`/api/booking`);
    const data=await response.json();
    if(data.data){
        let time="";
        fakeBody.style.display="block"
            if(data.data.time=="morning"){
                ampm="morning"
                time="早上 9 點到下午 4 點"
            }else{
                ampm="afternoon"
                time="下午 4 點到晚上 9 點"}
            attractionID=data.data.attraction.id
            imgJPG.setAttribute('src', data.data.attraction.image);
            attractionName.textContent=data.data.attraction.name;
            attractionDate.textContent=data.data.date;
            attractionTime.textContent=time;
            attractionPrice[0].textContent=data.data.price;
            attractionPrice[1].textContent=data.data.price;
            attractionAddress.textContent=data.data.attraction.address;
    }else{delBookingInfo()}
};
fetchBookingInfoAPI();

// delete booking info API
async function deleteAPI(){
    const response=await fetch(`/api/booking`, {method:"DELETE"});
    const data=await response.json();
    if(data.ok) return delBookingInfo();
};


function onSubmit() {
    // 讓 button click 之後觸發 getPrime 方法
    event.preventDefault();

    // 取得 TapPay Fields 的 status
    const tappayStatus = TPDirect.card.getTappayFieldsStatus();

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

async function sendPrimeToServer(prime){
    const response=await fetch(`/api/orders`,{
        method:"POST",
        body:JSON.stringify({
            "prime": prime,
            "order":{
                "price":attractionPrice[1].textContent,
                "trip":{
                    "attraction":{
                        "id": attractionID,
                        "name": attractionName.textContent,
                        "address": attractionAddress.textContent,
                        "image": imgJPG.src
                    }

                },
                "date": attractionDate.textContent,
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
    const data=await response.json();
    if(data.data){
        number=data.data.number
        deleteAPI()
        window.location.href=`/thankyou?number=${number}`;
    }
};

