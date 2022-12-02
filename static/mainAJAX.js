let fragment=document.createDocumentFragment();
let main=document.getElementById("main");
let page=0;
let keyword=null;
let isLoading=false;
let selectCatagoryList=document.getElementById("selectCatagoryList");
let listCatagory=document.getElementById("listCatagory");
//載入網頁，立刻執行抓取AIP
fetchAttractionsAPI();
//抓取API
function fetchAttractionsAPI(){
    isLoading=true; //正在載入
    // let urls="http://127.0.0.1:3000";
    let urls="http://13.112.252.173:3000";
    if (page==null) 
    return page==null;
    if (keyword==null){
        url=urls+"/api/attractions?page="+page
    }else{
        url=urls+"/api/attractions?page="+page+"&keyword="+keyword
    }
    fetch(url)
    .then(function(response){
        return response.json();
    })
    .then(function(data){
            if(data.data){
                for(let i=0; i< data.data.length; i++){
                    let mainDiv1=document.createElement("div");
                    mainDiv1.className="item";
                    //產出圖片
                    let mainImageBox=document.createElement("div");
                    mainImageBox.className="mainImageBox";
                    mainImageBox.addEventListener("click",()=>{
                        location.href=urls+"/attraction/"+data.data[i].id;
                    })
                    let mainImage=document.createElement("img");
                    mainImage.className="mainImage";
                    mainImage.setAttribute('src',data.data[i].images[0])
                    mainImageBox.appendChild(mainImage);
                    mainImageInBox=fragment.appendChild(mainImageBox);
                    //產出name
                    let nameBackground=document.createElement("div");
                    nameBackground.className="name-background";
                    let name=document.createElement("p");
                    name.appendChild(document.createTextNode(data.data[i].name));
                    name.className="name";
                    nameBackground.appendChild(name);
                    nameAndBackground=fragment.appendChild(nameBackground);
                    //產出mrt
                    let spanLeft=document.createElement("span");
                    spanLeft.appendChild(document.createTextNode(data.data[i].mrt));
                    spanLeft.className="mrt";
                    //產出cat
                    let spanRigth=document.createElement("span");
                    spanRigth.appendChild(document.createTextNode(data.data[i].category));
                    spanRigth.className="cat";
                    //裝進main
                    mainDiv1.append(mainImageInBox,nameAndBackground,spanLeft,spanRigth);
                    main.appendChild(fragment.appendChild(mainDiv1));
                }
            }
            page=data.nextPage;
            isLoading=false;
            //intersectionObserver 
            if(page!=null){
                // IntersectionObserver可以帶入兩個參數callback 和 options
                // callback可以帶入兩個參數
                let options={
                    root : null,
                    rootMargin: "0px 0px 0px 0px",
                    threshold: 0.8
                }
                let scroll=new IntersectionObserver((entries)=>{
                    if(isLoading==false){
                        if(entries[0].isIntersecting){
                            isLoading==false
                            fetchAttractionsAPI();
                        }
                    }
                },options);
                let footer=document.querySelector("footer");
                scroll.observe(footer)
            }
            //fetch第二個API，必須放在function裡才能work
            return fetch(urls+"/api/categories");
        }
    )
    .then(function(response){
        return response.json();
    }).then(function(data){
        //所有分類
        listCatagory.innerHTML=null
        for(let i=0;i<data.data.length;i++){
            let category=document.createElement("li");
            category.addEventListener("click",()=>{
                selectCatagoryList.value=data.data[i];
            });
            category.appendChild(document.createTextNode(data.data[i]));
            listCatagory.appendChild(fragment.appendChild(category));
        }
    });
};
// 展開景點分類
document.onclick=function(e){
    if(e.target.id != "listCatagory" & e.target.id !="selectCatagoryList" )
    {
        listCatagory.style.display="none";
    }else{
        listCatagory.style.display="grid";
    }
};
// keyword搜尋
function searchCategory(){
    main.innerHTML=null
    page=0
    keyword=document.querySelector("input").value
    fetchAttractionsAPI()
};