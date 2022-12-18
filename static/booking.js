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
                time="早上 9 點到下午 4 點"
            }else{time="下午 4 點到晚上 9 點"}
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
}