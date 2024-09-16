
var MenuItems = document.getElementById("MenuItems");

MenuItems.style.maxHeight = "0px";


function menutoggle() {
    if (MenuItems.style.maxHeight == "0px") {
            MenuItems.style.maxHeight = "200px";
        }
    else {
            MenuItems.style.maxHeight = "0px";
    }
}



var LoginForm = document.getElementById("LoginForm");
var RegForm = document.getElementById("RegistrForm");
var Indicator = document.getElementById("Indicator");

    function register(){
        RegistrForm.style.transform = "translateX(0px)";
        LoginForm.style.transform = "translateX(0px)";
        Indicator.style.transform = "translateX(100px)";
    }

    function login(){
        RegistrForm.style.transform = "translateX(300px)";
        LoginForm.style.transform = "translateX(300px)";
        Indicator.style.transform = "translateX(0px)";
    }





    /*!
* Start Bootstrap - Shop Homepage v5.0.6 (https://startbootstrap.com/template/shop-homepage)
* Copyright 2013-2023 Start Bootstrap
* Licensed under MIT (https://github.com/StartBootstrap/startbootstrap-shop-homepage/blob/master/LICENSE)
*/
// This file is intentionally blank
// Use this file to add JavaScript to your project