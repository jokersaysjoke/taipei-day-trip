const am=document.querySelector(".amButton");
const pm=document.querySelector(".pmButton");
const pathname=location.pathname;

// fetch API
fetchAttracionApi();
async function fetchAttracionApi(){
    const response=await fetch(`/api/${pathname}`);
    const data=await response.json();
    
    // create image
    const welcomeImgBox=document.querySelector(".welcome-imgbox")
    const welcomeImgBottom=document.querySelector(".welcome-img-bottom")
    if(data.data){
        for (let i=0;i<data.data.images.length; i++){
            // create image element
            const img=document.createElement("img");
            img.classList.add("welcomeImg");
            img.setAttribute('src', data.data.images[i]);
            welcomeImgBox.appendChild(img);

            // create imgButton
            const bottomButton=document.createElement("div");
            bottomButton.classList.add("welcome-img-bottom-button");
            //bind會生再生一個可填參數的function
            bottomButton.addEventListener('click',currentSlide.bind(null,i))
            welcomeImgBottom.appendChild(bottomButton);
        }
    }

    // create name
    const name=document.querySelector(".welcome-right-h2");
    name.textContent=data.data.name;

    // create cat at mrt
    const category=document.querySelector(".welcome-right-CatMrt");
    category.textContent=data.data.category+" at "+data.data.mrt

    // create description
    const description=document.querySelector(".description");
    description.textContent=data.data.description;

    // create address
    const address=document.querySelector(".address");
    address.textContent=data.data.address;

    // create transport
    const transport=document.querySelector(".transport");
    transport.textContent=data.data.transport;
    
    nextImg(index);
};
// toggle am、pm
const price=document.querySelector(".price")
document.onclick=function(button){
    if(button.target.className==="amButton"){
        am.style.backgroundColor="#448899";
        pm.style.backgroundColor="#ffffff";
        price.textContent="2000";

    }else if(button.target.className==="pmButton"){
        am.style.backgroundColor="#ffffff";
        pm.style.backgroundColor="#448899";
        price.textContent="2500";
    }
};

// previous、next image
let index=1;
function nextImg(n){
    const slide=document.querySelectorAll('.welcomeImg');
    const bottomButton=document.querySelectorAll(".welcome-img-bottom-button");
    if(n>slide.length){index=1}
    if(n<1){index=slide.length}
    for(let i=0; i<slide.length; i++){
        slide[i].style.display="none";
        bottomButton[i].className=bottomButton[i].className.replace(" active","");
    };
    slide[index-1].style.display="block";
    bottomButton[index-1].className +=" active";
};
function slideImg(n){
    nextImg(index+=n)
};
function currentSlide(n){
    nextImg(index=n+1)
};

// create reservation
const reservationButton=document.querySelector(".reservationButton");
const reservationDate=document.querySelector(".reservationDate");
reservationDate.valueAsDate=new Date()
const dateNull=document.querySelector(".dateNull");
const timeNull=document.querySelector(".timeNull");
let reservationTime="";
async function fetchBookingAPI(){
    const userResponse=await fetch(`/api/user/auth`);
    const userData=await userResponse.json();
    if(userData.data !==null){
        // 已經登入
        if(price.textContent==="2000"){
            reservationTime="morning";
        }else{reservationTime="afternoon"}
        fetch(`/api/booking`, {
            method:"POST",
            body:JSON.stringify({
                attractionId:parseInt(pathname.split("/").slice(-1)),
                date:reservationDate.value,
                time:reservationTime,
                price:price.innerText
            }),
            headers: new Headers({"Content-type":"application/json"})
        })
        .then(
            reservationButton.addEventListener("click", location.href=`/booking`)
        )
    }
    // 還沒登入
    else{openLogin()};
};
reservationButton.addEventListener("click", fetchBookingAPI);