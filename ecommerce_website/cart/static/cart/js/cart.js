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
            if (response.success && response.status === 'Quantity changed') {
                $('#base-price').html(`$${response.bill.base_price}`)
                if (response.bill.discount_amount) {
                    if ($('#discount-section').length) {
                        $('#discount-amount').html(`-$${response.bill.discount_amount}`);
                    } else {
                        $(`
                            <div class="row mt-4 mb-5" id="discount-section">
                                <div class="col">Discount</div>
                                <div class="col-auto fw-bold" id='discount-amount'>-$${response.bill.discount_amount}</div>
                            </div>
                        `).insertAfter('#items');
                    }
                } else {
                    $('#discount-section').remove();
                }


                if (!$('#price-after-discount').length && response.bill.discount_price < response.bill.base_price) {
                    $(`
                        <div class="row mt-4" id='price-after-discount'>
                            <div class="col">Price After Discounts</div>
                            <div class="col-auto fw-bold" id='discount-price'>$${response.bill.discount_price}</div>
                        </div>
                    `).insertBefore('#pickup');
                } else if ($('#price-after-discount').length && response.bill.discount_price < response.bill.base_price) {
                    $('#discount-price').html(`$${response.bill.discount_price}`);
                } else {
                    $('#price-after-discount').remove();
                }

                $('#discount-price').html(`$${response.bill.discount_price}`)
                $('#total-price').html(`$${response.bill.total_price}`)

                if (response.product.base_price > response.product.discount_price) {
                    $(`#${product}`).find('#product-price').html(`$${response.product.discount_price}`)
                    $(`#${product}`).find('#product-discount').html(`
                                        <div class="row fs-6 justify-content-end text-decoration-line-through">
                                            $${response.product.base_price}
                                        </div>
                                        <div class="row fs-6 fw-bold product-promotion justify-content-end">
                                            Save ${calculate_discount_saving(response.product.base_price, response.product.discount_price)}
                                        </div>
                    `)
                } else {
                    $(`#${product}`).find('#product-discount').empty()
                    $(`#${product}`).find('#product-price').html(`$${response.product.base_price}`)
                }
            }
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
        data: form.serialize() + `&product_slug=${product_slug}`,
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
    let product_id = form.find(('#data-input')).data('product')
    $.ajax({
        type: "POST",
        url: window.location.href + 'save-for-later/',
        data: form.serialize() + `&product_id=${product_id}`,
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
    let product_id = form.find(('#data-input')).data('product')
    $.ajax({
        type: "POST",
        url: window.location.href + 'move-to-cart/',
        data: form.serialize() + `&product_id=${product_id}`,
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
        data: form.serialize() + `&product_slug=${product_slug}`,
        success: function (response) {
            location.reload();
        },
        error: function (response) {
            console.log(response.success);
        }
    });
    return false;
});