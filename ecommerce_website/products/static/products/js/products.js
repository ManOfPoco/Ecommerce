function ratingCreation(id, rating) {
    $(function () {
        $('#' + id).rateYo({
            rating: rating,
            readOnly: true,
            starWidth: "20px"
        });
    });
}

word_rating = ['one_star', 'two_stars', 'three_stars', 'four_stars', 'five_stars']
for (let i = 4; i >= 0; i--) {
    ratingCreation(word_rating[i], i + 1)
}


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