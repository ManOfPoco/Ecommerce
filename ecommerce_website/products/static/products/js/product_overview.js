import { moveToCartAjax } from './snippets/ajax.js';

// initialize swiper for product images
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


// if user click on the product image the main one should be replaced with new one
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

// open selected image in the full page
let fullPage = document.getElementById('fullpage')
currentDisplaying.addEventListener('click', function () {
    fullPage.style.backgroundImage = 'url(' + currentDisplaying.src + ')';
    fullPage.style.display = 'block';
});


// hadnle collapsing product description and other product related sections
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

// create star rating function
function createRating(id, rating, starWidth = 20) {
    $(function () {
        $('#' + id).rateYo({
            rating: rating,
            readOnly: true,
            starWidth: `${starWidth}px`
        });
    });
}

// calculare percent of the progress bar line
function calculatePercent(number, searchingPercentNumber) {
    let percent = (searchingPercentNumber / number) * 100
    return percent
}

// initialize progress bar for product rating
let progressBarElements = document.getElementsByClassName('progress')
for (let i = 0; i < progressBarElements.length; i++) {
    let number = progressBarElements[i].getAttribute('aria-valuemax');
    let searchingPercentNumber = progressBarElements[i].getAttribute('aria-valuenow');

    let progressBar = progressBarElements[i].getElementsByClassName('progress-bar')[0];

    let percent = calculatePercent(number, searchingPercentNumber)
    progressBar.style.width = `${percent}%`
}

// initialize star rating for product
let productRating = document.getElementById('product-rating')
let productRatingDown = document.getElementById('product-rating-down')
if (productRating.getAttribute('data-rating') === '') {
    productRating.setAttribute('data-rating', 0)
}
createRating('product-rating', productRating.getAttribute('data-rating'), 14)
createRating('product-rating-down', productRating.getAttribute('data-rating'), 20)

// initialize star rating if there is Most Liked Positive Review and Most Liked Negative Review
let mostLikedPositiveReview = document.getElementById('most-liked-positive-review')
let mostLikedNegativeReview = document.getElementById('most-liked-negative-review')
if (mostLikedPositiveReview && mostLikedNegativeReview) {
    createRating('most-liked-positive-review', mostLikedPositiveReview.getAttribute('data-rating'), 20)
    createRating('most-liked-negative-review', mostLikedNegativeReview.getAttribute('data-rating'), 20)
}

// initialize star ratings for reviews
let productReviews = document.getElementsByName('product-reviews')
productReviews.forEach(review => {
    createRating(review.id, review.getAttribute('data-rating'))
});

// chose correct ordering option if user chose anything
const urlParams = new URLSearchParams(window.location.search);
function handleOrderingChange(ordering) {
    urlParams.set('ordering', ordering);
    const newUrl = window.location.pathname + '?' + urlParams.toString();

    window.location.href = newUrl;
}

// select corrent order option if user choise any
$('#ordering').on('change', function (e) {
    handleOrderingChange(this.value)
});

// scroll user to the reviews
function scrollReviews() {
    window.scrollTo({
        top: $("#customersReview").offset().top - 146,
        behavior: "smooth"
    });
}

// select correct ordering
const select = document.getElementById('ordering');
if (select && urlParams.has('ordering')) {
    for (let i = 0; i < select.options.length; i++) {
        let option = select.options[i];
        if (urlParams.get('ordering') === option.value) {
            option.selected = true;
            scrollReviews();
        }
    }
}
else if (urlParams.has('page')) {
    console.log(1);
    scrollReviews();
}

$('.anchor').on('click', function (e) {
    scrollReviews();
});


function calculate_discount_saving(regular_price, discount_price) {
    let discount_sum = (regular_price - discount_price).toFixed(2)
    let discount_percent = Math.round((discount_sum / regular_price) * 100)

    return `$${discount_sum} (${discount_percent}%)`
}

$('#product-quantity-form select').on('change', function (e) {
    let form = $(this).closest('form');
    let quantity = this.value

    $.ajax({
        type: "POST",
        url: window.location.href,
        data: form.serialize() + `&quantity=${quantity}`,
        success: function (response) {
            console.log(response.price);
            if (response.success && response.price) {
                if (response.price.discount_price) {
                    $('#price-section').html(`
                        <div class="row align-items-baseline" style="height:26px">
                            <div class="col-auto pe-0 fw-bold fs-2" style="font-family: 'Futura PT';" id='product-current-price'>
                                $${response.price.discount_price}
                            </div>
                            <div class="col ps-2 text-decoration-line-through align-bottom product-old-price" id='product-old-price'>
                                $${response.price.base_price}
                            </div>
                        </div>
                        <div class="row">
                            <div class="col product-promotion" id='product-discount'>
                                Save ${calculate_discount_saving(response.price.base_price, response.price.discount_price)}
                            </div>
                        </div>
                    `)
                } else if (!response.price.discount_price) {
                    $('#price-section').html(`
                        <div class="row align-items-baseline" style="height:26px">
                            <div class="col-auto pe-0 fw-bold fs-2" style="font-family: 'Futura PT';" id='product-current-price'>
                                ${response.price.base_price} 
                            </div>
                        </div>
                    `)
                }
            }
        },
        error: function (response) {
            console.log(response.success);
        }
    });
    return false;
})


// ajax like/dislike request
$('.reviewRateForm').on('submit', function (e) {
    let form = $(this)
    let option = form.find('button:focus').data('option');
    let oppositeOption = option === 'like' ? 'dislike' : 'like'
    $.ajax({
        type: "POST",
        url: '/review/rate-review/',
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
            if (!response.status) {
                form.find($('.form-messages')).html('<div class="alert alert-danger" id="usernameError">Something went wrong</div>')
            }
        },
        statusCode: {
            302: function () {
                window.location.href = "/account/sign-in/?next=" + window.location.href;
            }
        },
    });
    return false;
});


// initialize rating input for user
$(function () {
    $("<div class='error-message' style='display:none;'>Product Rating is required</div>").insertBefore("#div_id_product_rating")
    $("<label class='form-label requiredField'>Product Rating*</label>").insertBefore("#div_id_product_rating")
    $("#div_id_product_rating").addClass("ps-0");

    $("#div_id_product_rating").rateYo({
        rating: 0,
        fullStar: true
    });
});

// scroll user to the review form when button is clicked
$('#write-review-btn').click(function (e) {

    if ($('#review').css('display') === 'none') {
        $('#review').css('display', 'block')
        window.scrollTo({
            top: $("#review").offset().top - 146,
            behavior: "smooth"
        });
    } else {
        $('#review').css('display', 'none')
    }

})


// validate if user has chosen product rating
function validateRating(reviewRating) {
    if (reviewRating === 0) {
        $("<div class='alert alert-danger mb-3' id='required-rating'>Product Rating is required</div>").insertAfter("#div_id_product_rating")
        return false;
    } else if ($('#required-rating')) {
        $('#required-rating').css('display', 'none')
        return true;
    }
}

// ajax request for comment creation
$('#create-review-form').on('submit', function (e) {

    let form = $(this)
    let reviewRating = $("#div_id_product_rating").rateYo().rateYo("rating");
    if (!validateRating(reviewRating)) {
        return false
    }

    let product = window.location.href.split('/').slice(-2, -1)

    $.ajax({
        type: "POST",
        url: 'http://127.0.0.1:8000/review/write-review/',
        data: form.serialize() + `&product_rating=${reviewRating}` + `&product=${product}`,
        success: function (response) {
            if (response.success) {
                $('.review-messages').html("<div class='alert alert-success my-3' id='success-message'>Review was added</div>")
            }
            else {
                $('.review-messages').html("<div class='alert alert-danger my-3' id='error-message'>You can not comment the same product twice</div>")
            }
        },
        error: function (response) {
            if (!response.status) {
                $('.review-messages').html('<div class="invalid-feedback alert alert-danger d-block">Something went wrong</div>')
            }
        },
        statusCode: {
            302: function () {
                window.location.href = "/account/sign-in/?next=" + window.location.href;
            }
        },
    });
    return false;
});

// import ajax function for adding product to the wishlist via ajax request
$('.wishlist').on('click', function (e) {
    import('./snippets/ajax.js')
        .then(ajax => {
            ajax.wishlistAjax();
        })
});


// evoking ajax function for moving product to the cart via ajax request
moveToCartAjax();