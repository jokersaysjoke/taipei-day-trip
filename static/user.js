// let urls="http://127.0.0.1:3000";
let urls="http://13.112.252.173:3000";
let newUserName=document.querySelector(".newUserName");
let newEmail=document.querySelector(".newEmail");
let newPassword=document.querySelector(".newPassword");
let signMessage=document.querySelector(".signMessage");
let registerMessage=document.querySelector(".registerMessage");
// 註冊
function signUp(){
    if(newUserName.value=='' || newEmail.value=='' || newPassword.value==''){
        registerMessage.style.color="red";
        registerMessage.innerHTML="不可以空白";
    }
    else{
        fetch(urls+"/api/user",{
            method:"POST",
            body:JSON.stringify({
                name:newUserName.value,
                email:newEmail.value,
                password:newPassword.value
            }),
            headers: new Headers({"Content-type":"application/json"})
        })
        .then(function(response){
            return response.json();
        })
        .then(function(data){
            if(data.ok){
                registerMessage.style.color="green";
                registerMessage.innerHTML="註冊成功，請登入系統";}
            else if(data.error){
                registerMessage.style.color="red"
                registerMessage.innerHTML="email已經被註冊過"}
            else{
                registerMessage.style.color="red"
                registerMessage.innerHTML="連線錯誤"}
        })
    }
};
// 登入
let registerBoxEmail=document.querySelector(".registerBoxEmail")
let registerBoxPass=document.querySelector(".registerBoxPass")
function singIn(){
    fetch(urls+"/api/user/auth",{
        method:"PUT",
        body:JSON.stringify({
            email:registerBoxEmail.value,
            password:registerBoxPass.value
        }),
        headers: new Headers({"Content-type":"application/json"})
    })
    .then(function(response){
        return response.json();
    })
    .then(function(data){
        if(data.ok){
            signMessage.style.color="green";
            signMessage.innerHTML="登入成功";
            setTimeout("console.log('1')",1000)
            setTimeout("location.reload()",2000)
               
        }
        else if(data.error){
            signMessage.style.color="red"
            signMessage.innerHTML="email或密碼輸入錯誤"}
        else{
            signMessage.style.color="red"
            signMessage.innerHTML="連線錯誤"}
    })
};
//登出
let headerRightItem=document.querySelector("#headerRightItem")
function logOut(){
    fetch(urls+"/api/user/auth",{
        method:"DELETE"
    })
    .then(function(response){
        return response.json();
    })
    .then(function(data){
        if(data.ok){
            headerRightItem.innerHTML="登入/註冊"
            headerRightItem.addEventListener('click',(openLogin))
        }
    })
};

// 會員中
function member(){
    fetch(urls+"/api/user/auth")
    .then(function(response){
        return response.json();
    })
    .then(function(data){
        if(data.data != null){
            headerRightItem.innerHTML="登出系統";
            headerRightItem.addEventListener('click',logOut);
           
        }
        else{
            headerRightItem.innerHTML="登入/註冊";
            headerRightItem.addEventListener('click',(openLogin));
        }
    })
};
member();

// 打開、關閉註冊視窗
let loginWindow=document.querySelector("#login");
let registerWindow=document.querySelector("#register");
let registerWindowBackground=document.querySelector("#loginWindowBackground");
function openLogin(){
    loginWindow.style.display="block";
    registerWindowBackground.style.display="block";
};

let registerCloser=document.querySelector(".registerCloser");
function closeRegister(){
    // loginWindow.style.display="none";
    // registerWindow.style.display="none";
    // registerWindowBackground.style.display="none";
    location.reload();

};
function register(){
    registerWindow.style.display="block";
    loginWindow.style.display="none";
};
function login(){
    loginWindow.style.display="block";
    registerWindow.style.display="none";
    
};

