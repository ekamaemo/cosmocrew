let nextDom = document.getElementById('next');
let prevDom = document.getElementById('prev');
let carouselDom = document.querySelector('.slider');
let listItemDom = document.querySelector('.slider .list');

nextDom.onclick = function(){
    showSlider('next');
};
prevDom.onclick = function(){
    showSlider('prev');
};
let timeRunning = 3000;
let timeAutoNext = 7000;
let runTimeOut;
let runAutoRun;

function showSlider(type){
    let itemSlider = document.querySelectorAll('.slider .list .item');

    if(type === 'next'){
        listItemDom.appendChild(itemSlider[0]);
        carouselDom.classList.add('next');
    }else{
        let positionLastItem = 7;
        listItemDom.prepend(itemSlider[positionLastItem]);
        carouselDom.classList.add('prev');
    }
}
