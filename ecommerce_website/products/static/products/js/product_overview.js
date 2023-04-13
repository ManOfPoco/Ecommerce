const swiper = new Swiper('#productImages', {
    direction: 'horizontal',
    spaceBetween: 5,

    breakpoints: {
        300: { slidesPerView: 2 },
        500: { slidesPerView: 3 },
    },

    mousewheel: {
        invert: true,
    },

    navigation: {
        nextEl: '.swiper-button-next',
        prevEl: '.swiper-button-prev',
    },
});



let currentDisplaying = document.querySelector('#currentImg')
let currentSwiperImg = document.querySelector('.active-img')
let productImgs = document.querySelector('#productImages').getElementsByTagName('img')

for (const img of productImgs) {
    img.addEventListener('click', () => {
        if (img != currentSwiperImg) {
            currentSwiperImg.classList.remove('active-img')
            currentSwiperImg = img
            img.classList.add('active-img')
            currentDisplaying.src = img.src
        }
    })
}

let fullPage = document.getElementById('fullpage')
currentDisplaying.addEventListener('click', function () {
    fullPage.style.backgroundImage = 'url(' + currentDisplaying.src + ')';
    fullPage.style.display = 'block';
});


let ProductDetailsCollapses = document.querySelectorAll('.product-body-data')

for (const collapseSection of ProductDetailsCollapses) {

    let collapseElement = collapseSection.getElementsByClassName('collapse')
    let linkElem = collapseSection.getElementsByTagName('a')

    for (let i = 0; i < collapseElement.length; i++) {
        const collapse = collapseElement[i];
        const currentIcon = linkElem[i].getElementsByTagName('img')[0];

        collapse.addEventListener('show.bs.collapse', () => {
            currentIcon.src = collapseUpIcon
            currentIcon.alt = 'collapse-up'
        });

        collapse.addEventListener('hide.bs.collapse', () => {
            currentIcon.src = collapseDownIcon
            currentIcon.alt = 'collapse-down'
        });
    }
}

function createRating(id, rating, starWidth = 20) {
    $(function () {
        $('#' + id).rateYo({
            rating: rating,
            readOnly: true,
            starWidth: `${starWidth}px`
        });
    });
}

function calculatePercent(number, searchingPercentNumber) {
    let percent = (searchingPercentNumber / number) * 100
    return percent
}


let progressBarElements = document.getElementsByClassName('progress')
for (let i = 0; i < progressBarElements.length; i++) {
    let number = progressBarElements[i].getAttribute('aria-valuemax');
    let searchingPercentNumber = progressBarElements[i].getAttribute('aria-valuenow');

    let progressBar = progressBarElements[i].getElementsByClassName('progress-bar')[0];

    let percent = calculatePercent(number, searchingPercentNumber)
    progressBar.style.width = `${percent}%`
}

let productRating = document.getElementById('product-rating')
let productRatingDown = document.getElementById('product-rating-down')

if (productRating.getAttribute('data-rating') === '') {
    productRating.setAttribute('data-rating', 0)
}
createRating('product-rating', productRating.getAttribute('data-rating'), 14)
createRating('product-rating-down', productRating.getAttribute('data-rating'), 20)


let mostLikedPositiveReview = document.getElementById('most-liked-positive-review')
let mostLikedNegativeReview = document.getElementById('most-liked-negative-review')
if (mostLikedPositiveReview && mostLikedNegativeReview) {
    createRating('most-liked-positive-review', mostLikedPositiveReview.getAttribute('data-rating'), 20)
    createRating('most-liked-negative-review', mostLikedNegativeReview.getAttribute('data-rating'), 20)
}


let productReviews = document.getElementsByName('product-reviews')
productReviews.forEach(review => {
    createRating(review.id, review.getAttribute('data-rating'))
});

// choise correct ordering option if user chose anything
const urlParams = new URLSearchParams(window.location.search);
function handleOrderingChange(ordering) {
    urlParams.set('ordering', ordering);
    const newUrl = window.location.pathname + '?' + urlParams.toString();

    window.location.href = newUrl;
}

$('select').on('change', function (e) {
    handleOrderingChange(this.value)
});


function scrollReviews() {
    window.scrollTo({
        top: $("#customersReview").offset().top - 146,
        behavior: "smooth"
    });
}

// Select correct ordering
const select = document.getElementById('ordering')
if (select && urlParams.has('ordering')) {
    for (option of select) {
        if (urlParams.get('ordering') === option.value) {
            option.selected = true;
            scrollReviews();
        }
    }
}
else if (urlParams.has('page')) {
    scrollReviews();
}


$(document).ready(function () {

    $('form').on('submit', function (e) {
        let form = $(this)
        let option = form.find('button:focus').data('option');
        let oppositeOption = option === 'like' ? 'dislike' : 'like'
        $.ajax({
            type: "POST",
            url: window.location.href,
            data: $(this).serialize() + "&option=" + option,
            success: function (response) {

                let dataOption = `[data-option=${option}]`
                let OppositeDataOption = `[data-option=${oppositeOption}]`
                let basicSvg = option === 'like' ? likeSvg : dislikeSvg
                let fillSvg = option === 'like' ? likeFillSvg : dislikeFillSvg
                
                if (response.status === 'Created') {
                    form.find(`[data-option="${option}"]`).html(`<img src=${fillSvg} alt="${option}"> ${parseInt(form.find(dataOption).text()) + 1}`);
                }
                else if (response.status === 'Removed') {
                    form.find(`[data-option="${option}"]`).html(`<img src=${basicSvg} alt="${option}"> ${parseInt(form.find(dataOption).text()) - 1}`);
                }
                else if (response.status === 'Changed') {
                    let basicSvg = option === 'dislike' ? likeSvg : dislikeSvg
                    form.find(`[data-option="${option}"]`).html(`<img src=${fillSvg} alt="${option}"> ${parseInt(form.find(dataOption).text()) + 1}`);
                    form.find(`[data-option="${oppositeOption}"]`).html(`<img src=${basicSvg} alt="${oppositeOption}"> ${parseInt(form.find(OppositeDataOption).text()) - 1}`);
                }
            },
            error: function (response) {
                $('#reviewRateForm').after('<div class="invalid-feedback d-block" id="usernameError">Something went wrong</div>')
            }
        });
        return false;
    });
});