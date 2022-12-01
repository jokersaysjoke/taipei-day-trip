let am=document.querySelector(".amButton");
let pm=document.querySelector(".pmButton");
let price=document.querySelector(".price");
let pathname=location.pathname;
//載入頁面抓去API
fetchAttracionApi();
function fetchAttracionApi(){
    fetch("http://127.0.0.1:3000/api/"+pathname)
        .then(function(response){
            return response.json();
        })
        .then(function(data){
                //產出images
                let welcomeImgBox=document.querySelector(".welcome-imgbox")
                let welcomeImgBottom=document.querySelector(".welcome-img-bottom")
                for (let i=0;i<data.data.images.length; i++){
                    welcomeImg=document.createElement("img");
                    welcomeImg.className="welcomeImg";
                    welcomeImg.setAttribute('src', data.data.images[i]);
                    welcomeImgBox.appendChild(welcomeImg);
                    //產出imgButton
                    let bottomButton=document.createElement("div");
                    bottomButton.className=("welcome-img-bottom-button");
                    //bind會生再生一個可填參數的function
                    bottomButton.addEventListener('click',currentSlide.bind(null,i))
                    welcomeImgBottom.appendChild(bottomButton);
                }
                //產出name
                let name=document.querySelector(".welcome-right-h2");
                name.appendChild(document.createTextNode(data.data.name));
                //產出cat at mrt
                let category=document.querySelector(".welcome-right-CatMrt");
                category.appendChild(document.createTextNode(data.data.category+" at "+data.data.mrt));
                //產出description
                let description=document.querySelector(".description");
                description.appendChild(document.createTextNode(data.data.description));
                //產出address
                let address=document.querySelector(".address");
                address.appendChild(document.createTextNode(data.data.address));
                //產出transport
                let transport=document.querySelector(".transport");
                transport.appendChild(document.createTextNode(data.data.transport));
                nextImg(index);
        })

};

//上、下半天，切換
document.onclick=function(button){
    if(button.target.className=="amButton"){
        am.style.backgroundColor="#448899";
        pm.style.backgroundColor="#ffffff";
        price.innerHTML="新台幣 2000 元";

    }else if(button.target.className=="pmButton"){
        am.style.backgroundColor="#ffffff";
        pm.style.backgroundColor="#448899";
        price.innerHTML="新台幣 2500 元";
    }
};

//上、下一張image
let index=1;
function nextImg(n){
    //fetch完後，按funcion才會抓到length
    let slide=document.querySelectorAll('.welcomeImg');
    let bottomButton=document.querySelectorAll(".welcome-img-bottom-button");
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
