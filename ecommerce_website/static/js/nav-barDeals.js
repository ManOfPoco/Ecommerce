const banners = document.querySelectorAll('.banner')
let currentBannerIndex = 0;

function showNextBanner() {
    banners[currentBannerIndex].classList.remove('active')
    currentBannerIndex += 1
    if (currentBannerIndex >= banners.length) {
        currentBannerIndex = 0;
    }
    banners[currentBannerIndex].classList.add('active');
}

setInterval(showNextBanner, 5000)


const toggleSwiperBtn = document.getElementById('toggle-swiper');
const swiperHidden = document.querySelector('.hidden');
const swiperWraper = document.querySelector('.swiper-wrapper')


let dealsSwiper = new Swiper('#dealsSwiper', {
    direction: 'horizontal',
    slidesPerView: 3,
    loop: true,

    navigation: {
        nextEl: '.swiper-button-next',
        prevEl: '.swiper-button-prev',
    },

    observer: true,

});


toggleSwiperBtn.addEventListener('click', () => {
    if (swiperHidden.classList.contains('hidden')) {
        swiperWraper.style.position = 'relative'
        swiperHidden.classList.remove('hidden');
        swiperHidden.classList.add('showed');
    } else {
        swiperHidden.classList.remove('showed')
        swiperHidden.classList.add('hidden')
        setTimeout(() => {
            swiperWraper.style.position = 'absolute'
        }, 300)
    }
});

window.addEventListener('wheel', () => {
    if (swiperHidden.classList.contains('showed')) {
        swiperHidden.classList.remove('showed')
        swiperHidden.classList.add('hidden')
        setTimeout(() => {
            swiperWraper.style.position = 'absolute'
        }, 300)
    }
})