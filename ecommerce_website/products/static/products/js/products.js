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

// product cards rating
let productsRating = document.getElementsByName('product_rating')
productsRating.forEach(element => {
    let elemId = element.getAttribute('id')
    let elemValue = element.getAttribute('data-value')
    ratingCreation(elemId, elemValue, 15);
});

// check checkboxes
const checkboxes = document.querySelectorAll('input[type=checkbox]');
const urlParams = new URLSearchParams(window.location.search);

checkboxes.forEach(checkbox => {
    if (urlParams.has(checkbox.name) && urlParams.getAll(checkbox.name).includes(checkbox.value)) {
        checkbox.checked = true;
    }
});

// check if filter price is not equals 0. Set to 0 if it.
const minPriceCheckbox = document.querySelector('#minPrice')
const maxPriceCheckbox = document.querySelector('#maxPrice')

if (minPriceCheckbox.value === '') {
    minPriceCheckbox.value = 0;
}
if (urlParams.get('min_price') !== 0 && urlParams.get('min_price')) {
    minPriceCheckbox.value = urlParams.get('min_price');
}

if (maxPriceCheckbox.value === '') {
    maxPriceCheckbox.value = 0;
}
if (urlParams.get('max_price') !== 0 && urlParams.get('max_price')) {
    maxPriceCheckbox.value = urlParams.get('max_price');
}
