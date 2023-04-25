import { moveToCartAjax, wishlistAjax } from './snippets/ajax.js'

// create star ratings
function ratingCreation(id, rating, starWidth = 20) {
    $(function () {
        $('#' + id).rateYo({
            rating: rating,
            readOnly: true,
            starWidth: `${starWidth}px`
        });
    });
}

// filter rating
let wordRating = ['one_star', 'two_stars', 'three_stars', 'four_stars', 'five_stars']
let ratingCheckboxes = document.getElementsByName('reviews')
Array.from(ratingCheckboxes).reverse().forEach((checkbox, i) => {
    checkbox.setAttribute('value', i + 1)
    ratingCreation(wordRating[i], i + 1)
});

// initialize star rating for product cards
let productsRating = document.getElementsByName('product_rating')
productsRating.forEach(element => {
    let elemId = element.getAttribute('id')
    let elemValue = element.getAttribute('data-value')
    ratingCreation(elemId, elemValue, 15);
});

// if user choose any filters check those checkboxes 
const checkboxes = document.querySelectorAll('input[type=checkbox]');
const clearAllFilters = $('#clear-all')
const urlParams = new URLSearchParams(window.location.search);
const currentUrl = window.location.href

checkboxes.forEach(checkbox => {
    if (urlParams.has(checkbox.name) && urlParams.getAll(checkbox.name).includes(checkbox.value)) {
        checkbox.checked = true;
        clearAllFilters.show();

        // show applied filters
        let createdElement = addFilterToThePanel(checkbox.value)
        createdElement.on('click', (e) => {
            let newUrl = deleteUrlParam(checkbox.name, checkbox.value)

            let updatedUrlString = newUrl.toString();

            let updatedUrl = currentUrl.split("?")[0] + "?" + updatedUrlString;
            window.location.href = updatedUrl;
        })
    }
});


// if user chose any filters add them to the show panel
const appliedFilters = document.querySelector('#applied-filters');
function addFilterToThePanel(filterValue) {
    let id = filterValue.replaceAll(' ', '-')
    $('#applied-filters').prepend(`
        <div class="col-auto me-2 my-2 align-self-center applied-filter rounded-pill" id='${id}'>
            <div class="row">
                <div class="col-auto pe-0">
                    ${filterValue}
                </div>
                <div class="col-auto ps-1">
                    <img src="${closeImgUrl}" alt="close">
                </div>
            </div>
        </div>
    `)

    return $(`#${id}`)
}

// defele url params for specific key and value
function deleteUrlParam(delete_key, delete_value) {
    let urlParamsArray = []
    urlParams.forEach((value, key) => {
        if (key !== delete_key || value !== delete_value) {
            let keyComponent = encodeURIComponent(`${key}`)
            let valueComponent = encodeURIComponent(`${value}`)
            urlParamsArray.push(`${keyComponent}=${valueComponent}`)
        }
    });
    return urlParamsArray.join('&');
}

// check if there is something else except q(query for search) in the UrlParams. If there is, show clearAllFilters button
for (const key of urlParams.keys()) {
    if (key !== "q") {
        clearAllFilters.show();
        break;
    }
}

$('#filter-form').on('submit', function (e) {
    e.preventDefault();
    let search = urlParams.get('q')
    let updatedUrl = window.location.href.split("?")[0]
    let formData = $(this).serialize();

    if (search != null) {
        let url = updatedUrl + '?' + 'q=' + search + '&' + formData;
        window.location.href = url;
    } else {
        let url = updatedUrl + '?' + formData;
        window.location.href = url;
    }

});

// choose correct ordering option if user chose anything
function handleOrderingChange(ordering) {
    const urlParams = new URLSearchParams(window.location.search);
    urlParams.set('ordering', ordering);
    const newUrl = window.location.pathname + '?' + urlParams.toString();

    window.location.href = newUrl;
}

$('#ordering').on('change', function (e) {
    handleOrderingChange(this.value)
});

// select correct ordering
const select = document.getElementById('ordering');
if (select && urlParams.has('ordering')) {
    for (let i = 0; i < select.options.length; i++) {
        let option = select.options[i];
        if (urlParams.get('ordering') === option.value) {
            option.selected = true;
        }
    }
}


// set price values if there is any. delete urls params for price if they are default ones
const minPriceCheckbox = document.querySelector('#minPrice')
const maxPriceCheckbox = document.querySelector('#maxPrice')
if (!urlParams.get('min_price')) {
    minPriceCheckbox.value = 0
} else {
    minPriceCheckbox.value = urlParams.get('min_price')
}
if (!urlParams.get('max_price')) {
    maxPriceCheckbox.value = maxPriceCheckbox.value
} else {
    maxPriceCheckbox.value = urlParams.get('max_price')
}
if (urlParams.get('min_price') == 0 && urlParams.get('max_price') == maxPriceCheckbox.value) {
    urlParams.delete('min_price')
    urlParams.delete('max_price')
}

// import ajax function for adding product to the wishlist via ajax request
$('.wishlist').on('click', function (e) {
    wishlistAjax();
});

// evoking ajax function for moving product to the cart via ajax request
moveToCartAjax();
