function ratingCreation(id, rating, starWidth=20) {
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
for (let i = 0; i < 5; i++) {
    let checkbox = ratingCheckboxes[i];
    ratingCreation(wordRating[checkbox.value - 1], i + 1)
}

// product cards rating
let productsRating = document.getElementsByName('product_rating')
productsRating.forEach(element => {
    let elemId = element.getAttribute('id')
    let elemValue = element.getAttribute('data-value')
    ratingCreation(elemId, elemValue, 15);
});

const checkboxes = document.querySelectorAll('input[type=checkbox]');
const urlParams = new URLSearchParams(window.location.search);

checkboxes.forEach(checkbox => {
    if (urlParams.has(checkbox.name) && urlParams.getAll(checkbox.name).includes(checkbox.value)) {
        checkbox.checked = true;
    }
});

const minPriceCheckbox = document.querySelector('#minPrice')
const maxPriceCheckbox = document.querySelector('#maxPrice')

if (minPriceCheckbox.value === '') {
    minPriceCheckbox.value = 0;
}
if (maxPriceCheckbox.value === '') {
    maxPriceCheckbox.value = 0;
}

if (urlParams.get('price_from') !== 0 && urlParams.get('price_from')) {
    minPriceCheckbox.value = urlParams.get('price_from');
}

if (urlParams.get('price_to') !== 0 && urlParams.get('price_from')) {
    maxPriceCheckbox.value = urlParams.get('price_to');
}