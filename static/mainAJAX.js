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
                        
                            let mainImage=document.createElement("img");
                            mainImage.className="mainImage";
                            mainImage.setAttribute('src',data.data[i].images[0]);
                            
                            let spanLeft=document.createElement("span");
                            spanLeft.appendChild(document.createTextNode(data.data[i].mrt));
                            spanLeft.className="mrt";
                        
                            let spanRigth=document.createElement("span");
                            spanRigth.appendChild(document.createTextNode(data.data[i].category));
                            spanRigth.className="cat";
                        
                            mainDiv1.append(mainImage,spanLeft,spanRigth);
                            fragment.appendChild(mainDiv1);
                        }
                        main.appendChild(fragment);
                    
                    }

                })

