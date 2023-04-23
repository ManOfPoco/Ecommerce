import { moveToCartAjax } from './snippets/ajax.js'

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

// product cards rating
let productsRating = document.getElementsByName('product_rating')
productsRating.forEach(element => {
    let elemId = element.getAttribute('id')
    let elemValue = element.getAttribute('data-value')
    ratingCreation(elemId, elemValue, 15);
});

// if user chose any filters check those checkboxes 
const checkboxes = document.querySelectorAll('input[type=checkbox]');
const appliedFilters = document.querySelector('#applied-filters');
const clearAllFilters = document.querySelector('#clear-all')
const urlParams = new URLSearchParams(window.location.search);
const currentUrl = window.location.href

checkboxes.forEach(checkbox => {
    if (urlParams.has(checkbox.name) && urlParams.getAll(checkbox.name).includes(checkbox.value)) {
        checkbox.checked = true;

        // show applied filters
        let createdElement = addFilterToThePanel(checkbox.value, appliedFilters, clearAllFilters)
        createdElement.addEventListener('click', () => {

            let newUrl = deleteUrlParam(checkbox.name, checkbox.value)

            let updatedUrlString = newUrl.toString();
            let updatedUrl = currentUrl.split("?")[0] + "?" + updatedUrlString;
            window.location.href = updatedUrl;
        })
    }
});

// if user chose any filters add them to the show panel
function addFilterToThePanel(filterValue, insertIntoElement, parentElement) {
    // Create the main div
    let mainDiv = document.createElement("div");
    mainDiv.classList.add("col-auto", 'me-2', 'my-2', "align-self-center", 'applied-filter', 'rounded-pill');

    // Create the inner row div
    let innerDiv = document.createElement("div");
    innerDiv.classList.add("row");

    // Create the first column div
    let firstColDiv = document.createElement("div");
    firstColDiv.classList.add("col-auto", "pe-0");
    firstColDiv.textContent = filterValue;

    // Create the second column div
    let secondColDiv = document.createElement("div");
    secondColDiv.classList.add("col-auto", "ps-1");

    // Create the image element
    let imgElement = document.createElement("img");
    imgElement.src = closeImgUrl;
    imgElement.alt = "close";

    // Append the image element to the second column div
    secondColDiv.appendChild(imgElement);

    // Append the first and second column divs to the inner row div
    innerDiv.appendChild(firstColDiv);
    innerDiv.appendChild(secondColDiv);

    // Append the inner row div to the main div
    mainDiv.appendChild(innerDiv);

    // Append the main div to a parent element on the page
    insertIntoElement.insertBefore(mainDiv, parentElement);

    return mainDiv;
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

// choise correct ordering option if user chose anything
function handleOrderingChange(ordering) {
    const urlParams = new URLSearchParams(window.location.search);
    urlParams.set('ordering', ordering);
    const newUrl = window.location.pathname + '?' + urlParams.toString();

    window.location.href = newUrl;
}

$('#ordering').on('change', function (e) {
    handleOrderingChange(this.value)
});

// Select correct ordering
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


const minPriceCheckbox = document.querySelector('#minPrice')
const maxPriceCheckbox = document.querySelector('#maxPrice')

// set checkbox values if there is not any. delete urls params for price if they are default ones
function setCheckboxValue(checkbox, paramName, defaultValue) {
    if (checkbox.value === '') {
        checkbox.value = defaultValue;
    }
    const paramValue = urlParams.get('min_price');
    if (paramValue !== defaultValue && paramValue) {
        checkbox.value = paramValue;
    }
    if (checkbox.value === checkbox.min) {
        urlParams.delete(paramName);
    }
    if (checkbox.value === checkbox.max) {
        urlParams.delete(paramName);
    }
}

setCheckboxValue(minPriceCheckbox, 'min_price', 0);
setCheckboxValue(maxPriceCheckbox, 'max_price', 0);

// hide clearAllFilters if user didn't specify price
if (minPriceCheckbox.value === minPriceCheckbox.min && maxPriceCheckbox.value === maxPriceCheckbox.max && clearAllFilters) {
    clearAllFilters.style.display = 'none'
}

// import ajax function for adding product to the wishlist via ajax request
$('.wishlist').on('click', function (e) {
    import('./snippets/ajax.js')
        .then(ajax => {
            ajax.wishlistAjax();
        })
});

// evoking ajax function for moving product to the cart via ajax request
moveToCartAjax();
