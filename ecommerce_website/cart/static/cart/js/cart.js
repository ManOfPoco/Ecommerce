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
    let old_price = formInput.data('old-price')
    let base_bill_price = parseFloat(($('#base-price').text()).split('$')[1])
    let discount_amount = ($('#discount-amount').text()).split('$')[1]

    $.ajax({
        type: "POST",
        url: window.location.href,
        data: form.serialize() + `&old_quantity=${old_quantity}` + `&new_quantity=${new_quantity}` + `&product_slug=${product}` + `&total_price=${base_bill_price}` + `&old_price=${old_price}` + `&discount_amount=${discount_amount}`,
        success: function (response) {

            if (response.success && response.status === 'Quantity changed') {
                $('#base-price').html(`$${response.bill.bill_base_price}`)
                $('#total-price').html(`$${response.bill.total_price}`)
                $('#discount-amount').html(`-$${response.bill.discount_amount}`)
                $('#discount-price').html(`$${response.bill.bill_discount_price}`)
                let productCard = $(`#${product}`)
                productCard.find('#product-price').html(`$${response.bill.current_price}`)
                if (response.bill.base_product_price != response.bill.current_price)
                productCard.find('#product-discount').html(`<div class="row fs-6 justify-content-end text-decoration-line-through">
                                                            $${response.bill.base_product_price}
                                                        </div>
                                                        <div class="row fs-6 fw-bold product-promotion justify-content-end">
                                                            Save ${calculate_discount_saving(response.bill.base_product_price, response.bill.current_price)}
                                                        </div>`)
                else {
                    productCard.find('#product-discount').html('')
                }
                form.removeData();
                formInput.data('old-quanitity', new_quantity)
                formInput.data('old-price', response.bill.current_price)
            }
            console.log(response.bill);
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