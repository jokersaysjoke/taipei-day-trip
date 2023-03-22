async function fetchOrderHistory(){
    const response=await fetch(`/api/account`);
    const data=await response.json();
    if(data.data){
        let time="";
        if(data.data.time==="morning"){
            ampm="morning"
            time="早上 9 點到下午 4 點"
        }else{
            ampm="afternoon"
            time="下午 4 點到晚上 9 點"}
        for(let i=0; i<data.data.length; i++){
            // create img
            const imgBox=document.createElement("div");
            imgBox.classList.add("img-box");
            const img=document.createElement("img");
            img.classList.add("order-img")
            img.setAttribute("src", data.data[i]["image"])
            imgBox.appendChild(img)

            // create p element
            const p1=document.createElement("p");
            p1.innerHTML=`訂單編號: <span>${data.data[i]["number"]}</span>`;
            p1.classList.add("order-number");
            
            const p2=document.createElement("p");
            p2.innerHTML=`景點名稱: <span>${data.data[i]["name"]}</span>`;

            const p3=document.createElement("p");
            p3.innerHTML=`導覽日期: <span>${data.data[i]["date"]}</span>`;
            
            const p4=document.createElement("p");
            p4.innerHTML=`導覽時間: <span>${time}</span>`;

            const p5=document.createElement("p");
            p5.innerHTML=`導覽費用: <span>${data.data[i]["price"]}</span>`;
           
            // append to detail div
            const detail=document.createElement("div");
            detail.classList.add("order-info-detail");
            detail.append(p1, p2, p3, p4, p5);
            
            // append to orderInfo div
            const orderInfo=document.createElement("div");
            orderInfo.classList.add("order-info");
            orderInfo.append(imgBox, detail);
            
            // create main
            const accountMain=document.querySelector(".account-main");
            accountMain.appendChild(orderInfo);
        }        
    }
};
// fetch ordered
fetchOrderHistory();

// toggle userInfo、ordered
document.onclick=function(click){
    if(click.target.id==="account-header-user"){
        const accountMain=document.querySelector(".account-main");
        accountMain.innerHTML=""
    }else if(click.target.id==="account-header-order"){
        location.reload();
    }
};