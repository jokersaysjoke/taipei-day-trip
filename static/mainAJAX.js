fetch("http://127.0.0.1:3000/api/attractions?page=0")
.then(function(response){
    return response.json();
})
.then(function(data){
                    
                    // console.log(data);
                    if(data.nextPage!=null){
                        let main=document.getElementById("main");
                        let fragment=document.createDocumentFragment();
                        for(let i=0; i< data.data.length; i++){
                            let mainDiv1=document.createElement("div");
                            mainDiv1.className="item";
    
                            let mainImageBox=document.createElement("div");
                            mainImageBox.className="mainImageBox";
                            let mainImage=document.createElement("img");
                            mainImage.className="mainImage";
                            mainImage.setAttribute('src',data.data[i].images[0])
                            mainImageBox.appendChild(mainImage);
                            mainImageInBox=fragment.appendChild(mainImageBox);
    
    
                            let nameBackground=document.createElement("div");
                            nameBackground.className="name-background";
                            let name=document.createElement("p");
                            name.appendChild(document.createTextNode(data.data[i].name));
                            name.className="name";
                            nameBackground.appendChild(name);
                            nameAndBackground=fragment.appendChild(nameBackground);
    
                            let spanLeft=document.createElement("span");
                            spanLeft.appendChild(document.createTextNode(data.data[i].mrt));
                            spanLeft.className="mrt";
    
                            let spanRigth=document.createElement("span");
                            spanRigth.appendChild(document.createTextNode(data.data[i].category));
                            spanRigth.className="cat";
    
                            mainDiv1.append(mainImageInBox,nameAndBackground,spanLeft,spanRigth);
                            fragment.appendChild(mainDiv1);
                        }
                        main.appendChild(fragment);
                    
                    }

                })

