function calculate_discount_saving(regular_price, discount_price) {
    let discount_sum = (regular_price - discount_price).toFixed(2)
    let discount_percent = Math.round((discount_sum / regular_price) * 100)

    return `$${discount_sum} (${discount_percent}%)`
}


$('.quanitity-select-form select').on('change', function (e) {
    let form = $(this).closest('form');
    let formInput = form.find('#quanitity-data')
    
    let product = formInput.data('product')
    let new_quantity = this.value
    let old_quantity = formInput.data('old-quanitity')

    $.ajax({
        type: "POST",
        url: window.location.href,
        data: form.serialize() + `&old_quantity=${old_quantity}` + `&new_quantity=${new_quantity}` + `&product_slug=${product}`,
        success: function (response) {

            location.reload();
        },
        error: function (response) {
            console.log(response.success);
        }
    });
    return false;
})


$('.cart-item-remove').on('submit', function (e) {
    let form = $(this);
    let product_slug = form.find(('#data-input')).data('product')
    $.ajax({
        type: "POST",
        url: window.location.href + 'cart-item-remove/',
        data: form.serialize() + `&product_slug=${product_slug}` ,
        success: function (response) {
            location.reload();
        },
        error: function (response) {
            console.log(response.success);
        }
    });
    return false;
});


$('.save-for-later').on('submit', function (e) {
    let form = $(this);
    let product_slug = form.find(('#data-input')).data('product')
    $.ajax({
        type: "POST",
        url: window.location.href + 'save-for-later/',
        data: form.serialize() + `&product_slug=${product_slug}` ,
        success: function (response) {
            location.reload();
        },
        error: function (response) {
            console.log(response.success);
        }
    });
    return false;
});


$('.move-to-cart').on('submit', function (e) {
    let form = $(this);
    let product_slug = form.find(('#data-input')).data('product')
    $.ajax({
        type: "POST",
        url: window.location.href + 'move-to-cart/',
        data: form.serialize() + `&product_slug=${product_slug}` ,
        success: function (response) {
            location.reload();
        },
        error: function (response) {
            console.log(response.success);
        }
    });
    return false;
});


$('.save-for-later-remove').on('submit', function (e) {
    let form = $(this);
    let product_slug = form.find(('#data-input')).data('product')
    $.ajax({
        type: "POST",
        url: window.location.href + 'save-for-later-remove/',
        data: form.serialize() + `&product_slug=${product_slug}` ,
        success: function (response) {
            location.reload();
        },
        error: function (response) {
            console.log(response.success);
        }
    });
    return false;
});