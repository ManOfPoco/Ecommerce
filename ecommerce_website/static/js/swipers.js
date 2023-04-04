function createSwiper(swiperIdName) {

    let topTrendingProducts = new Swiper(`#${swiperIdName}`, {
        direction: 'horizontal',
        loop: true,

        autoplay: {
            delay: 4000,
        },

        breakpoints: {
            540: { slidesPerView: 2 },
            960: { slidesPerView: 3 },
            1140: { slidesPerView: 4 },
            1320: { slidesPerView: 5 },
        },

        navigation: {
            nextEl: '.swiper-button-next',
            prevEl: '.swiper-button-prev',
        },

    });
}

createSwiper('customersPrefer');
