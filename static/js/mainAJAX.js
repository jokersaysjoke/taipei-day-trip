let url;
let page=0;
let keyword=null;
let isLoading=false;
const main=document.querySelector("#main")
const listCatagory=document.querySelector("#listCatagory");
const selectCatagoryList=document.querySelector("#selectCatagoryList");
selectCatagoryList.focus();

// 載入網頁立刻 fetch API
window.onload = fetchAttractionsAPI;

// fetch API
async function fetchAttractionsAPI(){
    isLoading=true; // 正在載入
    if (page===null) return page===null;
    if (keyword===null){
        url=`/api/attractions?page=${page}`;
    }else{
        url=`/api/attractions?page=${page}&keyword=${keyword}`;
    }
    const mainResponse=await fetch(url);
    const mainData=await mainResponse.json();
    if(mainData.data){
        page=mainData.nextPage;
        isLoading=false;
        const data=mainData.data;
        for(let i=0; i< data.length; i++){
            // create main div element
            const mainDivEl=document.createElement("div");
            mainDivEl.classList.add("item");

            // create main image box element
            const mainImageBox=document.createElement("div");
            mainImageBox.classList.add("mainImageBox");
            mainImageBox.addEventListener("click", () => {
                location.href=`/attraction/${data[i].id}`;
            })
            
            // create main image element
            const mainImage=document.createElement("img");
            mainImage.classList.add("mainImage");
            mainImage.setAttribute("src", data[i].images[0])
            mainImageBox.appendChild(mainImage);

            // create name background element
            const nameBackground=document.createElement("div");
            nameBackground.classList.add('name-background');

            // create name element
            const name=document.createElement("p");
            name.classList.add("name");
            name.textContent=data[i].name;
            nameBackground.appendChild(name);

            // create mrt elment
            const mrt=document.createElement("span");
            mrt.classList.add("mrt");
            mrt.textContent=data[i].mrt;

            // create category element
            const cat=document.createElement("span");
            cat.classList.add("cat");
            cat.textContent=data[i].category;

            // 裝進 maindiv
            mainDivEl.append(mainImageBox, nameBackground, mrt, cat);

            // 裝進 #main
            main.appendChild(mainDivEl);
        }
        //intersectionObserver 
        if(page!=null){
            // IntersectionObserver可以帶入兩個參數callback 和 options
            // callback可以帶入兩個參數
            const options={
                root : null,
                rootMargin: "0px 0px 0px 0px",
                threshold: 0.8
            };
            const scroll=new IntersectionObserver((entries)=>{
                if(isLoading===false){
                    if(entries[0].isIntersecting){
                        isLoading=false
                        fetchAttractionsAPI();
                    }
                }
            }, options);
            const footer=document.querySelector("footer");
            scroll.observe(footer)
        }
    }

    // fetch second API
    const categoryResponse=await fetch(`/api/categories`);
    const categoryData=await categoryResponse.json();

    // 所有分類
    listCatagory.innerHTML=null
    if(categoryData.data){
        const data=categoryData.data;
        for(let i=0;i<data.length;i++){
            const category=document.createElement("li");
            category.addEventListener("click", () => {
                selectCatagoryList.value=data[i];
            });
            category.textContent=data[i];
            listCatagory.appendChild(category);
        }
    }
};

// open catagory window
document.onclick=function(e){
    if(e.target.id !== "listCatagory" & e.target.id !=="selectCatagoryList" )
    {
        listCatagory.style.display="none";
    }else{
        listCatagory.style.display="grid";
    }
};

// keyword search
function searchCategory(){
    main.innerHTML=null
    page=0
    keyword=selectCatagoryList.value
    fetchAttractionsAPI()
};
selectCatagoryList.addEventListener('keydown', (event)=>{
    if (event.keyCode === 13) {
        searchCategory();
    }
})