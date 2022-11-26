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
    isLoading=true;
    if (page==null) 
    return page==null;
    if (keyword==null){
        url="http://127.0.0.1:3000/api/attractions?page="+page
    }else{
        url="http://127.0.0.1:3000/api/attractions?page="+page+"&keyword="+keyword
    }
    fetch(url)
    .then(function(response){
        return response.json();
    })
    .then(function(data){
            if(data.data){
                page=data.nextPage;
                for(let i=0; i< data.data.length; i++){
                    let mainDiv1=document.createElement("div");
                    mainDiv1.className="item";
                    //產出圖片
                    let mainImageBox=document.createElement("div");
                    mainImageBox.className="mainImageBox";
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
            //fetch第二個API
            return fetch("http://127.0.0.1:3000/api/categories");
        }
    )
    .then(function(response){
        return response.json();
    }).then(function(data){
        //所有分類
        listCatagory.innerHTML=null
        for(let i=0;i<data.data.length;i++){
            let category=document.createElement("li");
            category.className="gategoryName";
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
    if(e.target.id != "listCatagory" & e.target.id !="selectCatagoryList" & e.target.className !="gategoryName")
    {
        listCatagory.style.display="none";
    }else{
        listCatagory.style.display="grid";
    }
};
// 載入nextPage
function renderNextPage(){
  
};
// keyword搜尋
function searchCategory(){
    main.innerHTML=null
    page=0
    keyword=document.querySelector("input").value
    console.log(keyword);
    fetchAttractionsAPI()
};


// window.addEventListener("scroll",renderNextPage);         
// window.pageYOffset 垂直移動量
// window.innerHeight 回傳瀏覽器 (broswer) 視窗內的網頁內容高度。
// document.body.clientHeight視窗的高度
// document.body.offsetHeight
