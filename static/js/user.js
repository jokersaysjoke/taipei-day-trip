const newUserName=document.querySelector(".newUserName");
const newEmail=document.querySelector(".newEmail");
const newPassword=document.querySelector(".newPassword");
const signMessage=document.querySelector(".signMessage");
const registerMessage=document.querySelector(".registerMessage");
// 註冊
function signUp(){
    if(newUserName.value=='' || newEmail.value=='' || newPassword.value==''){
        registerMessage.style.color="red";
        registerMessage.innerHTML="不可以空白";
    }
    else{
        fetch(`/api/user`,{
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
const registerBoxEmail=document.querySelector(".registerBoxEmail");
const registerBoxPass=document.querySelector(".registerBoxPass");

function singIn(){
    fetch(`/api/user/auth`,{
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
            setTimeout("location.reload()",500)
               
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
const headerRightItem=document.querySelector("#headerRightItem")
function logOut(){
    fetch("/api/user/auth",{
        method:"DELETE"
    })
    .then(function(response){
        return response.json();
    })
    .then(function(data){
        if(data.ok){
            headerRightItem.innerHTML="登入/註冊"
            setTimeout("location.reload()",500)
            headerRightItem.addEventListener('click',(openLogin))
        }
    })
};
const reservation=document.querySelector(".header-rightItem")
// 會員中
function member(){
    fetch(`/api/user/auth`)
    .then(function(response){
        return response.json();
    })
    .then(function(data){
        if(data.data != null){
            //已登入
            headerRightItem.innerHTML="登出系統";
            headerRightItem.addEventListener('click',logOut);
            reservation.innerHTML='<a href=/booking>預定行程</a>';
        }
        else{
            //未登入
            headerRightItem.innerHTML="登入/註冊";
            headerRightItem.addEventListener('click',(openLogin));
            reservation.addEventListener('click',(openLogin));
        }
    })
};
member();

// 打開、關閉註冊視窗
const loginWindow=document.querySelector("#login");
const registerWindow=document.querySelector("#register");
const registerWindowBackground=document.querySelector("#loginWindowBackground");
function openLogin(){
    loginWindow.style.display="block";
    registerWindowBackground.style.display="block";
    registerBoxEmail.focus();
};

const registerCloser=document.querySelector(".registerCloser");
function closeRegister(){
    location.reload();
};
function register(){
    registerWindow.style.display="block";
    loginWindow.style.display="none";
    newUserName.focus();
};
function login(){
    loginWindow.style.display="block";
    registerWindow.style.display="none";
    
};

