$(document).ready(function(){
    document.getElementsByClassName("nav__navigation")[0].style.visibility="hidden"

    var navcount = 0

    document.getElementsByClassName("nav__btn__label")[0].addEventListener("click", function(){
        navcount=navcount + 1
    })

    document.getElementsByClassName("nav__navigation")[0].addEventListener("transitionend", function(){
        if (navcount % 2 == 0){
            document.getElementsByClassName("nav__navigation")[0].style.visibility="hidden"
            navcount=0
        }
    })

    document.getElementsByClassName("nav__navigation")[0].addEventListener("transitionstart", function(){
        if (navcount % 2 == 1){
            document.getElementsByClassName("nav__navigation")[0].style.visibility="visible"
        }
    })
})