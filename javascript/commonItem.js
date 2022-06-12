export function printCommonItem(onNavList) {

    printHead().then(function (){
    });

    printHeader().then(function (){
        for(let i = 0; i < onNavList.length; i++){
            const onNav = document.querySelector("#" + onNavList[i] + "Nav");
            onNav.classList.add("bl_tabNav_link__is_active");
        }
    });

    printFooter().then(function (){
    });

}

function printHead() {
    let head = new Promise(function (resolve) {
        fetch("./../commonItem/head.html")
        .then(function (response) {
            return response.text();
        })
        .then(function (data) {
            document.querySelector("head").innerHTML = data + document.querySelector("head").innerHTML;
            resolve();
        })
    });
    return head;
}

function printHeader() {
    let header = new Promise(function (resolve) {
        fetch("./../commonItem/header.html")
        .then(function (response) {
            return response.text();
        })
        .then(function (data) {
            document.querySelector("header").innerHTML = data;
            // const workNav = document.querySelector("#workNav");
            // const studyNav = document.querySelector("#studyNav");
            // const tipsNav = document.querySelector("#tipsNav");
            // const diaryNav = document.querySelector("#diaryNav");
            // const styleNav = document.querySelector("#styleNav");
            resolve();
        })
    });

    return header;
};

function printFooter() {
    let footer = new Promise(function (resolve) {
        fetch("./../commonItem/footer.html")
        .then(response => {
            return response.text();
        })
        .then(data => {
            document.querySelector("footer").innerHTML = data;
            resolve();
        })
    });

    return footer;
};